/*
CJK CMS based on CodeRed CMS
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

/**
 * Main script which is used to detect Cms features requiring JavaScript.
 *
 * Loads the necessary libraries for that feature, then initializes any
 * feature-specific code. This should only be used for features that might be
 * site-wide (e.g. StreamField blocks that could occur anywhere). For
 * functionality that is page-specific, include the JavaScript normally via a
 * script tag on that page instead.
 *
 * This file must run with "pure" JavaScript - assume jQuery or any other
 * scripts are not yet loaded.
 */
const cjkcms_libs = {
    masonry: {
      url: "https://cdn.jsdelivr.net/npm/masonry-layout@4.2.2/dist/masonry.pkgd.min.js",
      integrity: "sha256-Nn1q/fx0H7SNLZMQ5Hw5JLaTRZp0yILA/FRexe19VdI=",
    },
  };
  
  /**
   * Dynamically loads a script and/or CSS from the `lib` object above.
   *
   * Put functionality related to the script you are loading into the `success`
   * callback of the `load_script` function. Otherwise, it might not work as
   * intended.
   */
  function load_script(lib, success) {
    var head = document.getElementsByTagName("head")[0];
    if (lib.head) {
      // Create a temporary element and insert the `lib.head` string to form a
      // child element.
      var tmpEl = document.createElement("div");
      tmpEl.innerHTML = lib.head;
      // Append the child element to the `<head>`
      head.append(tmpEl.firstElementChild);
    }
    if (lib.url) {
      // Fetch and execute the script in the global context.
      // Then call the `success` callback.
      fetch(lib.url, {
        integrity: lib.integrity,
        referrerPolicy: "origin",
      })
        .then(function (response) {
          return response.text();
        })
        .then(function (txt) {
          // Eval in the global scope.
          eval?.(txt);
        })
        .then(function () {
          if (success) {
            success();
          }
        });
    }
  }

document.addEventListener("DOMContentLoaded", function() {
    /*** Link handling ***/
    if(typeof cjkcms_external_new_tab !== 'undefined' && cjkcms_external_new_tab) {

        const elems = document.getElementsByTagName('a');
        for (let i = 0; i < elems.length; i++) {
            let href = elems[i]['href'].trim();
            if (
                !href.startsWith(cjkcms_site_url) &&
                !href.startsWith('/') &&
                !href.startsWith('#') &&
                !href.startsWith('?'))
            {
                elems[i]['target'] = '_blank';
            }
        }
    }

    /*** Lightbox ***/

    const gallery_images = document.getElementsByClassName('lightbox-preview');
    Array.from(gallery_images,el => el.addEventListener('click', event => {
        let orig_src = event.target.getAttribute('data-original-src')
        let orig_alt = event.target.getAttribute('alt')
        let orig_ttl = event.target.getAttribute('title')
        let lightbox_id = event.target.getAttribute('data-modal-id')
        const img = document.getElementById('lightbox-image-'+lightbox_id)
        img.setAttribute('src', orig_src);
        img.setAttribute('alt', orig_alt);
        img.setAttribute('title', orig_ttl);
    }));

    /** Tracking **/
    
    if (typeof cms_track_clicks !== "undefined" && cms_track_clicks) {
        document.querySelectorAll("a").forEach(function (el) {
            el.addEventListener("click", function (event) {
            var el = event.currentTarget;
            gtag_data = {
                event_category: "Link",
                event_label: el.textContent.trim().substring(0, 30),
            };
            if (el.dataset.gaEventCategory) {
                gtag_data["event_category"] = el.dataset.gaEventCategory;
            }
            if (el.dataset.gaEventLabel) {
                gtag_data["event_label"] = el.dataset.gaEventLabel;
            }
            gtag("event", "click", gtag_data);
            });
        });
    }

    /** Masonry **/
    if (document.querySelectorAll("[data-masonry]").length > 0) {
        load_script(cjkcms_libs.masonry);
    }

    /** Film Strip Controls **/
    let strips = document.querySelectorAll("[data-block='film-strip']");
    strips.forEach((el) => {
        const leftButton = el.querySelector("[data-button='left']");
        const rightButton = el.querySelector("[data-button='right']");
        const container = el.querySelector("[data-block='film-container']");

        leftButton.addEventListener("click", function () {
            const panels = el.querySelectorAll("[data-block='film-panel']");
            let currentBlock = parseInt(el.dataset.currentBlock) - 1;
            if (currentBlock < 0) currentBlock = panels.length - 1;
            el.dataset.currentBlock = currentBlock;

            const elem = panels[currentBlock];
            const left = elem.offsetLeft;

            container.scroll({ top: 0, left: left, behavior: "smooth" });
        });

        rightButton.addEventListener("click", function () {
            const panels = el.querySelectorAll("[data-block='film-panel']");
            let currentBlock = parseInt(el.dataset.currentBlock) + 1;
            if (currentBlock >= panels.length) currentBlock = 0;
            el.dataset.currentBlock = currentBlock;

            const elem = panels[currentBlock];
            const left = elem.offsetLeft;

            container.scroll({ top: 0, left: left, behavior: "smooth" });
        });
    });

});

