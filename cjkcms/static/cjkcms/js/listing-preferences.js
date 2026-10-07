(() => {
    const initialise = (form) => {
        if (form.dataset.enhanced || !form.dataset.resultsUrl) return;
        form.dataset.enhanced = 'true';
        form.querySelector('[data-listing-apply]').hidden = true;
        // Listings without optional columns only offer the page size.
        const shortcuts = form.querySelector('[data-listing-shortcuts]');
        if (shortcuts) shortcuts.hidden = false;
        const status = form.querySelector('[data-listing-status]');
        const retry = form.querySelector('[data-listing-retry]');
        const toggles = () => form.querySelectorAll('input[name="visible_columns"]');
        let pending = null;
        let saving = false;
        let lastAction = 'apply';

        const listingUrl = () => {
            const url = new URL(form.action);
            // Wagtail reflects AJAX search/filter state in the browser URL.
            url.search = window.location.search;
            url.searchParams.delete(form.dataset.pageParameter || 'p');
            url.searchParams.delete('export');
            return url;
        };

        const refreshListing = async () => {
            // Search may change while preferences are saving. Only replace
            // results for the current query and the latest submitted choices.
            while (!pending) {
                const url = listingUrl();
                const resultsUrl = new URL(form.dataset.resultsUrl, window.location.href);
                resultsUrl.search = url.search;
                const response = await fetch(resultsUrl, {
                    credentials: 'same-origin',
                    headers: {'X-Requested-With': 'XMLHttpRequest'},
                });
                if (!response.ok || response.redirected) throw new Error('Listing refresh failed');
                const html = await response.text();
                if (pending) return;
                if (url.href !== listingUrl().href) continue;
                const results = document.getElementById('listing-results');
                results.innerHTML = html;
                window.history.replaceState(window.history.state, '', url);
                // Reinitialize Wagtail bulk actions, filters and listing widgets.
                results.dispatchEvent(new CustomEvent('w-swap:success', {
                    bubbles: true,
                    detail: {requestUrl: resultsUrl.href, results: html},
                }));
                return;
            }
        };

        const save = async () => {
            if (saving) return;
            saving = true;
            try {
                // Serialize writes rather than aborting requests that may have
                // already reached the server. Rapid toggles coalesce to the
                // latest snapshot, so an older save cannot win the race.
                while (pending) {
                    const data = pending;
                    pending = null;
                    status.textContent = form.dataset.savingMessage;
                    status.removeAttribute('data-error');
                    retry.hidden = true;
                    const response = await fetch(listingUrl(), {
                        method: 'POST', body: data, credentials: 'same-origin',
                        headers: {'Accept': 'application/json'},
                    });
                    if (!response.ok || response.redirected) throw new Error('Preference save failed');
                    const result = await response.json();
                    if (!result.saved) throw new Error('Preference save failed');
                    await refreshListing();
                }
                status.textContent = form.dataset.savedMessage;
            } catch {
                pending = null;
                status.textContent = form.dataset.errorMessage;
                status.setAttribute('data-error', '');
                retry.hidden = false;
            } finally {
                saving = false;
            }
        };

        const queue = (action = 'apply') => {
            lastAction = action;
            pending = new FormData(form);
            pending.set('listing_preferences_action', action);
            save();
        };

        form.addEventListener('change', (event) => {
            if (event.target.matches('[name="visible_columns"], [name="page_size"]')) queue();
        });
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const action = event.submitter?.value || 'apply';
            if (action === 'reset') {
                toggles().forEach((toggle) => { toggle.checked = true; });
                form.elements.page_size.value = '';
            }
            queue(action);
        });
        form.addEventListener('click', (event) => {
            const show = event.target.closest('[data-listing-show-all]');
            const hide = event.target.closest('[data-listing-hide-all]');
            if (show || hide) {
                toggles().forEach((toggle) => { toggle.checked = Boolean(show); });
                queue();
            }
            if (event.target.closest('[data-listing-retry]')) queue(lastAction);
        });
    };

    const start = () => document.querySelectorAll('[data-listing-preferences-form]').forEach(initialise);
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start, {once: true});
    } else {
        start();
    }
})();
