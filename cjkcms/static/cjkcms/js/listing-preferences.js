(() => {
    document.addEventListener('submit', (event) => {
        const form = event.target.closest('[data-listing-preferences-form]');
        if (!form) return;
        // Wagtail search and filters update the browser URL without replacing
        // the header. Use that current query when saving display options.
        const action = new URL(form.action);
        action.search = window.location.search;
        action.searchParams.delete(form.dataset.pageParameter || 'p');
        action.searchParams.delete('export');
        form.action = action.href;
    });

    document.addEventListener('keydown', (event) => {
        if (event.key !== 'Escape') return;
        document.querySelectorAll('.cjkcms-listing-preferences[open]').forEach((menu) => {
            menu.open = false;
            menu.querySelector('summary').focus();
        });
    });

    document.addEventListener('click', (event) => {
        document.querySelectorAll('.cjkcms-listing-preferences[open]').forEach((menu) => {
            if (!menu.contains(event.target)) menu.open = false;
        });
    });
})();
