pref("browser.search.defaultenginename", "Heexy");
pref("browser.search.defaultenginename", "Heexy");
//
/*
 * If you make changes to your about:config while the program is running, the
 * changes will be overwritten by the user.js when the application restarts.
 *
 * To make lasting changes to preferences, you will have to edit the user.js.
 */

/****************************************************************************
 * Betterfox                                                                *
 * "Ad meliora"                                                             *
 * version: 129                                                             *
 * url: https://github.com/yokoffing/Betterfox                              *
 * Betterfox by yokoffing, edited by Heexy
****************************************************************************/

/****************************************************************************
 * SECTION: FASTFOX                                                         *
****************************************************************************/
/** GENERAL ***/
pref("content.notify.interval", 100000);

/** GFX ***/
pref("gfx.canvas.accelerated.cache-items", 4096);
pref("gfx.canvas.accelerated.cache-size", 512);
pref("gfx.content.skia-font-cache-size", 20);

/** DISK CACHE ***/
pref("browser.cache.jsbc_compression_level", 3);

/** MEDIA CACHE ***/
pref("media.memory_cache_max_size", 65536);
pref("media.cache_readahead_limit", 7200);
pref("media.cache_resume_threshold", 3600);

/** IMAGE CACHE ***/
pref("image.mem.decode_bytes_at_a_time", 32768);

/** NETWORK ***/
pref("network.http.max-connections", 1800);
pref("network.http.max-persistent-connections-per-server", 10);
pref("network.http.max-urgent-start-excessive-connections-per-host", 5);
pref("network.http.pacing.requests.enabled", false);
pref("network.dnsCacheExpiration", 3600);
pref("network.ssl_tokens_cache_capacity", 10240);

/** SPECULATIVE LOADING ***/
pref("network.dns.disablePrefetch", true);
pref("network.dns.disablePrefetchFromHTTPS", true);
pref("network.prefetch-next", false);
pref("network.predictor.enabled", false);
pref("network.predictor.enable-prefetch", false);

/** EXPERIMENTAL ***/
pref("layout.css.grid-template-masonry-value.enabled", true);
pref("dom.enable_web_task_scheduling", true);
pref("dom.security.sanitizer.enabled", true);

/****************************************************************************
 * SECTION: SECUREFOX                                                       *
****************************************************************************/
/** TRACKING PROTECTION ***/
pref("browser.contentblocking.category", "strict");
pref("urlclassifier.trackingSkipURLs", "*.reddit.com, *.twitter.com, *.twimg.com, *.tiktok.com"); // allow embedded tweets, Instagram and Reddit posts, and TikTok embeds
pref("urlclassifier.features.socialtracking.skipURLs", "*.instagram.com, *.twitter.com, *.twimg.com");
pref("network.cookie.sameSite.noneRequiresSecure", true);
pref("browser.download.start_downloads_in_tmp_dir", true); // less cache
pref("browser.helperApps.deleteTempFileOnExit", true); // less cache
pref("browser.uitour.enabled", false); // disable uitour backend
pref("browser.uitour.url", ""); // WILL cause console errors - better safety
pref("privacy.globalprivacycontrol.enabled", true);
pref("security.sandbox.gpu.level", 1); // DISABLE IF BUILDING A LINUX BUILD
pref("privacy.partition.bloburl_per_partition_key", true); // making network partitioning better
pref("privacy.bounceTrackingProtection.enabled", true); // bounce tracker protection
pref("privacy.bounceTrackingProtection.enableDryRunMode", false); // false enables tracker data purging
pref("browser.send_pings", false);
pref("dom.battery.enabled", false); // disable permission for websites to get devices current battery level
pref("devtools.debugger.remote-enabled", false); // disable remote debugging
pref("privacy.globalprivacycontrol.enabled", true); // make a request to visited site, that the user doesn't want any of his data sold and/or gathered. Respected by many sites
pref("privacy.globalprivacycontrol.functionality.enabled", true);
pref("privacy.globalprivacycontrol.pbmode.enabled", true);

/** OCSP & CERTS / HPKP ***/
// disable oscp -- explanation by yokoffing in betterfox.js/securefox: OCSP leaks your IP and domains you visit to the CA when OCSP Stapling is not available on visited host.
// OCSP is vulnerable to replay attacks when nonce is not configured on the OCSP responder.
pref("security.OCSP.enabled", 0);
pref("security.remote_settings.crlite_filters.enabled", true);
pref("security.pki.crlite_mode", 2);
pref("security.cert_pinning.enforcement_level", 1); // allow user's mitm(antivirus) to verify certificates

/** SSL / TLS ***/
pref("security.ssl.treat_unsafe_negotiation_as_broken", true);
pref("browser.xul.error_pages.expert_bad_cert", true);
pref("security.tls.enable_0rtt_data", false);

// FPP (WiP)
pref("privacy.resistFingerprinting.randomization.daily_reset.enabled", true); // enable fpp
pref("privacy.resistFingerprinting.randomization.daily_reset.private.enabled", true); // enable fpp in incognito

/** DISK AVOIDANCE ***/
pref("browser.privatebrowsing.forceMediaMemoryCache", true); //prevent media cache from writing to disk in Private Browsing
pref("browser.sessionstore.interval", 60000); // save the current state of the session every minute
pref("browser.pagethumbnails.capturing_disabled", true); // disable capturing thumbnails

/** SHUTDOWN & SANITIZING ***/
pref("privacy.history.custom", true);

/** SEARCH / URL BAR ***/
pref("browser.urlbar.trimHttps", true);
pref("browser.urlbar.untrimOnUserInteraction.featureGate", true);
pref("browser.search.separatePrivateDefault.ui.enabled", true);
pref("browser.urlbar.update2.engineAliasRefresh", true);
pref("browser.search.suggest.enabled", true);
pref("browser.urlbar.quicksuggest.enabled", true);
pref("browser.urlbar.suggest.quicksuggest.sponsored", false);
pref("browser.urlbar.suggest.quicksuggest.nonsponsored", false);
pref("browser.urlbar.groupLabels.enabled", false);
pref("browser.formfill.enable", false);
pref("security.insecure_connection_text.enabled", true);
pref("security.insecure_connection_text.pbmode.enabled", true);
pref("network.IDN_show_punycode", true);

/** HTTPS-FIRST POLICY ***/
pref("dom.security.https_first", true);

/** PASSWORDS + FORMS***/
pref("signon.formlessCapture.enabled", false);
pref("signon.privateBrowsingCapture.enabled", false);
pref("network.auth.subresource-http-auth-allow", 1);
pref("editor.truncate_user_pastes", false);
pref("layout.forms.reveal-password-button.enabled", true); // enable always shown password reveal button
pref("signon.rememberSignons", false);
pref("signon.rememberSignons.visibilityToggle", true); // DEFAULT
pref("signon.schemeUpgrades", true); // DEFAULT
pref("signon.showAutoCompleteFooter", false); // DEFAULT
pref("signon.autologin.proxy", false); // DEFAULT
pref("extensions.formautofill.creditCards.enabled", false); // don't store credit card information locally
pref("extensions.formautofill.addresses.enabled", false); // don't store address information locally

/** MIXED CONTENT + CROSS-SITE ***/
pref("security.mixed_content.block_display_content", true);
pref("pdfjs.enableScripting", false);
pref("extensions.postDownloadThirdPartyPrompt", false);


/** HEADERS / REFERERS ***/
pref("network.http.referer.XOriginTrimmingPolicy", 2);

/** CONTAINERS ***/
pref("privacy.userContext.ui.enabled", true);

/** WEBRTC ***/
pref("media.peerconnection.ice.proxy_only_if_behind_proxy", true);
pref("media.peerconnection.ice.default_address_only", true);

/** SAFE BROWSING ***/
pref("browser.safebrowsing.downloads.remote.enabled", false);

/** MOZILLA ***/
pref("permissions.default.desktop-notification", 2);
pref("permissions.default.geo", 2);
pref("permissions.manager.defaultsUrl", "");
pref("webchannel.allowObject.urlWhitelist", "");

/** TELEMETRY ***/
pref("datareporting.policy.dataSubmissionEnabled", false);
pref("datareporting.healthreport.uploadEnabled", false);
pref("toolkit.telemetry.unified", false);
pref("toolkit.telemetry.enabled", false);
pref("toolkit.telemetry.server", "data:,");
pref("toolkit.telemetry.archive.enabled", false);
pref("toolkit.telemetry.newProfilePing.enabled", false);
pref("toolkit.telemetry.shutdownPingSender.enabled", false);
pref("toolkit.telemetry.updatePing.enabled", false);
pref("toolkit.telemetry.bhrPing.enabled", false);
pref("toolkit.telemetry.firstShutdownPing.enabled", false);
pref("toolkit.telemetry.coverage.opt-out", true);
pref("toolkit.coverage.opt-out", true);
pref("toolkit.coverage.endpoint.base", "");
pref("browser.newtabpage.activity-stream.feeds.telemetry", false);
pref("browser.newtabpage.activity-stream.telemetry", false);
pref("dom.security.unexpected_system_load_telemetry_enabled", false);
pref("messaging-system.rsexperimentloader.enabled", false);
pref("network.trr.confirmation_telemetry_enabled", false);
pref("security.app_menu.recordEventTelemetry", false);
pref("security.certerrors.mitm.priming.enabled", false);
pref("security.certerrors.recordEventTelemetry", false);
pref("security.protectionspopup.recordEventTelemetry", false);
pref("signon.recipes.remoteRecipes.enabled", false);
pref("privacy.trackingprotection.emailtracking.data_collection.enabled", false);

/** EXPERIMENTS ***/
pref("app.shield.optoutstudies.enabled", false);
pref("app.normandy.enabled", false);
pref("app.normandy.api_url", "");

/** CRASH REPORTS ***/
pref("breakpad.reportURL", "");
pref("browser.tabs.crashReporting.sendReport", false);
pref("browser.crashReports.unsubmittedCheck.autoSubmit2", false);

/** DETECTION ***/
pref("captivedetect.canonicalURL", "");
pref("network.captive-portal-service.enabled", false);
pref("network.connectivity-service.enabled", false);

/****************************************************************************
 * SECTION: PESKYFOX                                                        *
****************************************************************************/
/** MOZILLA UI ***/
pref("browser.privatebrowsing.vpnpromourl", "");
pref("extensions.getAddons.showPane", false); // disables recommended addons, which means no google analytics usage
pref("extensions.htmlaboutaddons.recommendations.enabled", false); //disables recommended addons in about:addons, which means no google analytics usage
pref("browser.discovery.enabled", false); // Personalized Extension Recommendations in about:addons and AMO
pref("browser.shell.checkDefaultBrowser", false); // disables the "set hxy_browser as your default browser" thingy
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false); // disables contextual feature recommendations in addons
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false); // disables contextual feature recommendations in features?
pref("browser.preferences.moreFromMozilla", true); // hides "more from Mozilla" text in settings
pref("browser.aboutConfig.showWarning", false); // removes the annoying warning in about:config
pref("browser.aboutwelcome.enabled", true); // enables welcome page(about:welcome)
pref("browser.tabs.tabmanager.enabled", false); // better tab organization with more tabs
pref("browser.profiles.enabled", true); // new profile switcher -- idk what that means

/** THEME ADJUSTMENTS ***/
pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // enable Firefox to use userChome, userContent, etc.
pref("browser.compactmode.show", true);  // adds compact mode back
pref("layout.css.prefers-color-scheme.content-override", 2); // make the preferred theme for websites "dark"
pref("browser.privateWindowSeparation.enabled", true); // WINDOWS -- seems to have no effect
pref("browser.newtabpage.activity-stream.newtabWallpapers.v2.enabled", true); // new tab wallpapers

/** COOKIE BANNER HANDLING ***/
// if possible reject cookie banners. If not keep them on screen
pref("cookiebanners.service.mode", 1);
pref("cookiebanners.service.mode.privateBrowsing", 1);

/** FULLSCREEN NOTICE ***/
pref("full-screen-api.transition-duration.enter", "0 0");
pref("full-screen-api.transition-duration.leave", "0 0");
pref("full-screen-api.warning.delay", -1);
pref("full-screen-api.warning.timeout", 0);

/** URL BAR ***/
pref("browser.urlbar.suggest.calculator", true);
pref("browser.urlbar.unitConversion.enabled", true);
pref("browser.urlbar.trending.featureGate", false);

/** NEW TAB PAGE ***/
pref("browser.newtabpage.activity-stream.feeds.topsites", false);
pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);

/** POCKET ***/
pref("extensions.pocket.enabled", false);

/** DOWNLOADS ***/
pref("browser.download.manager.addToRecentDocs", false);

/** PDF ***/
pref("browser.download.open_pdf_attachments_inline", true);

/** TAB BEHAVIOR ***/
pref("browser.bookmarks.openInTabClosesMenu", false);
pref("browser.menu.showViewImageInfo", true);
pref("findbar.highlightAll", true);
pref("layout.word_select.eat_space_to_next_word", false);

/** speed nyyyomth ***/
pref("content.notify.interval", 100000); // (.10s); default=120000 (.12s) - reflow interval - should be <= 0.1
pref("browser.cache.disk.enable", true); //should be default, disable if storage problems
pref("browser.cache.disk.max_entry_size", 91200); //increases max object size in disk cache to improve efficiency on spinny drives
pref("network.http.rcwn.enabled", false); //decrease network usage. !!WILL RENDER CACHE REALLY SLOW ON SPINNY DRIVES!!
pref("browser.cache.disk.metadata_memory_limit", 1000); // default=250 (0.25 MB); improves spinny drives efficiency
pref("browser.cache.disk.preload_chunk_count", 5); // DEFAULT 4 - make lower for lower ram usage
pref("browser.cache.disk.max_chunks_memory_usage", 50960); // DEFAULT 40 MB; lets more things get into cache, so more cache hits for big cache data
pref("browser.cache.disk.max_priority_chunks_memory_usage", 38000); // DEFAULT 40 MB; slightly decreased, so important cache files don't miss on spinny drives
pref("browser.cache.disk.free_space_soft_limit", 10240); // default=5120 (5 MB). ungarbles ur cache
pref("browser.cache.disk.free_space_hard_limit", 2048); // default=1024 (1 MB)
pref("browser.cache.jsbc_compression_level", 2); // makes cached js bytecode slightly compressed - helps with cache size
//pref("browser.cache.memory.capacity", -1); // DEFAULT; 256000=256 MB; 512000=500 MB; 1048576=1GB, 2097152=2GB
//pref("browser.cache.memory.max_entry_size", 10240); // (10 MB); default=5120 (5 MB)
pref("browser.sessionhistory.max_total_viewers", 5); // balances ram usage with session history(bach button) speed
pref("media.cache_size", 628000); // DEFAULT=512000; for some reason lowers ram usage, also huge speed improvement for SSDs
pref("media.memory_cache_max_size", 65536); // default=8192; AF=65536; alt=131072; ungarbles ur cache
pref("media.memory_caches_combined_limit_pc_sysmem", 5); // default=5;
pref("media.mediasource.enabled", true); // DEFAULT; this is here to prevent (built-in)plugins breaking videos
pref("media.cache_readahead_limit", 7200); // 120 min; default=60; stop reading ahead when our buffered data is this many seconds ahead of the current playback - increases ram usage, but makes unstable networks usable
pref("media.cache_resume_threshold", 3600); // 60 min; default=30; when a network connection is suspended, don't resume it until the amount of buffered data falls below this threshold
pref("image.mem.decode_bytes_at_a_time", 32768); // default=16384; alt=65536; chunk size for calls to the image decoders
pref("network.buffer.cache.count", 128); // default=24; increases the maximum number of cache entries for packets
pref("network.http.max-connections", 1800); // default=900
pref("network.http.max-persistent-connections-per-server", 10); // default=6; download connections; anything above 10 is excessive for the average user
pref("network.http.max-urgent-start-excessive-connections-per-host", 5); // default=3
//pref("network.http.pacing.requests.enabled", false); UNCOMMENT WHEN BROWSER RUNS SMOOTHLY ON THE LOWEST OF LOWEST DEVICES
pref("network.dnsCacheEntries", 1100); // default=400; can make dns resolving faster
pref("network.dnsCacheExpiration", 7200); // keep entries for 2 hours
pref("network.dnsCacheExpirationGracePeriod", 240); // default=60; cache DNS entries for 4 minutes after they expire
pref("network.ssl_tokens_cache_capacity", 10240); // default=2048; more TLS token caching (fast reconnects)
pref("network.dns.disablePrefetch", true);
    pref("network.dns.disablePrefetchFromHTTPS", false); // [FF127+ false]
pref("browser.low_commit_space_threshold_mb", 3276); // default=200; ONLY WINDOWS AND MACOS
pref("dom.ipc.processPrelaunch.fission.number", 2); // default=3; Process Preallocation Cache
pref("fission.webContentIsolationStrategy", 2);
pref("browser.preferences.defaultPerformanceSettings.enabled", false);
    pref("dom.ipc.processCount.webIsolated", 1); // one process per site origin (high value)
    pref("dom.ipc.processCount", 8); // determine by number of CPU cores/processors

/****************************************************************************
 * SECTION: SMOOTHFOX                                                       *
****************************************************************************/
// visit https://github.com/yokoffing/Betterfox/blob/main/Smoothfox.js
// Enter your scrolling overrides below this line:
pref("apz.overscroll.enabled", true);
pref("general.smoothScroll", true);
pref("general.smoothScroll.msdPhysics.enabled", true);
pref("mousewheel.default.delta_multiplier_y", 280);

/****************************************************************************
 * END: BETTERFOX                                                           *
****************************************************************************/

// pref("browser.urlbar.update2.engineAliasRefresh"
pref("browser.tabs.hoverPreview.showThumbnails", false);

//********************************************************************************

// Heexy Speed fox

// Disable Animations (Not noticable)
pref("browser.tab.animate", false); // Disables tab switching animations
// Performance improvment settings
pref("browser.panorama.animate_zoom", false); // Disables zoom animations in tab groups (Panorama)
pref("browser.download.animateNotifications", false); // Speeds up download process by disabling animations
pref("security.dialog_enable_delay", 0); // Removes delay for security dialog display
pref("network.prefetch-next", false); // Stops prefetching to reduce bandwidth usage
pref("layers.acceleration.disabled", true); // Disables hardware acceleration to avoid potential GPU-related performance issues
pref("network.http.use-cache", true); // Enables caching of HTTP content for faster page loading
pref("browser.cache.disk.capacity", 1048576); // Increases disk cache size to 1GB for better storage of cached data
pref("browser.tabs.remote.autostart", false); // Disables multiprocess tabs for lower system resource usage on weak hardware
pref("browser.cache.offline.enable", false); // Disables offline cache to ensure faster loading from the network
pref("browser.transitions.enabled", false); // Disables animations between page transitions to improve responsiveness
pref("network.image.http.accept", "image/webp,*/*;q=0.8"); // Prefers loading faster and compressed WebP images
pref("network.http.pipelining", true); // Enables HTTP pipelining for parallel request handling
pref("network.http.pipelining.maxrequests", 8); // Limits max simultaneous HTTP requests to 8 for balanced performance
pref("network.http.connection-timeout", 10); // Sets a shorter connection timeout to avoid slow connections
pref("network.dns.disableIPv6", true); // Disables IPv6 to reduce DNS lookup time and improve connection speed
pref("places.history.enabled", false); // Disables browsing history to reduce resource usage
pref("browser.formfill.enable", false); // Disables form autofill to speed up form-heavy page loads
// Design
pref("nglayout.enable_drag_images", false); // Disable tab preview when you moving with tabs