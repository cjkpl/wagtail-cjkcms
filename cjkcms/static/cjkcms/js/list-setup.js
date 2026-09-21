(function () {
    function initListSetup() {
        const openBtn = document.getElementById('list-setup-open');
        const modal = document.getElementById('list-setup-modal');
        const closeBtn = document.getElementById('list-setup-close');
        const applyBtn = document.getElementById('list-setup-apply');
        const resetBtn = document.getElementById('list-setup-reset');
        const list = document.getElementById('list-setup-columns');
        const perPageSelect = document.getElementById('list-setup-per-page');

        if (!openBtn || !modal || !applyBtn || !list) {
            return;
        }

        openBtn.addEventListener('click', function (e) {
            e.preventDefault();
            modal.style.display = 'block';
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                modal.style.display = 'none';
            });
        }

        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });

        let dragged = null;
        list.querySelectorAll('li').forEach(function (item) {
            item.addEventListener('dragstart', function () {
                dragged = item;
                item.style.opacity = '0.6';
            });
            item.addEventListener('dragend', function () {
                item.style.opacity = '1';
            });
            item.addEventListener('dragover', function (e) {
                e.preventDefault();
            });
            item.addEventListener('drop', function (e) {
                e.preventDefault();
                if (!dragged || dragged === item) {
                    return;
                }
                const rect = item.getBoundingClientRect();
                const before = (e.clientY - rect.top) < (rect.height / 2);
                if (before) {
                    list.insertBefore(dragged, item);
                } else {
                    list.insertBefore(dragged, item.nextSibling);
                }
            });
        });

        applyBtn.addEventListener('click', function () {
            const selected = [];
            list.querySelectorAll('li').forEach(function (li) {
                const checkbox = li.querySelector('input[type="checkbox"]');
                if (checkbox && checkbox.checked) {
                    selected.push(li.dataset.col);
                }
            });

            const url = new URL(window.location.href);
            url.searchParams.delete('p');
            if (selected.length) {
                url.searchParams.set('cols', selected.join(','));
            } else {
                url.searchParams.delete('cols');
            }
            if (perPageSelect && perPageSelect.value) {
                url.searchParams.set('per_page', perPageSelect.value);
            }
            window.location.href = url.toString();
        });

        if (resetBtn) {
            resetBtn.addEventListener('click', function () {
                const url = new URL(window.location.href);
                url.searchParams.delete('p');
                url.searchParams.delete('cols');
                url.searchParams.delete('per_page');
                window.location.href = url.toString();
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initListSetup);
    } else {
        initListSetup();
    }
})();
