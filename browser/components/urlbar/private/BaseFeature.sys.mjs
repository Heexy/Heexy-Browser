/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const lazy = {};

ChromeUtils.defineESModuleGetters(lazy, {
  QuickSuggest: "resource:///modules/QuickSuggest.sys.mjs",
  UrlbarPrefs: "resource:///modules/UrlbarPrefs.sys.mjs",
  UrlbarUtils: "resource:///modules/UrlbarUtils.sys.mjs",
});

/**
 * Base class for quick suggest features. It can be extended to implement a
 * feature that is part of the larger quick suggest feature and that should be
 * enabled only when quick suggest is enabled.
 *
 * You can extend this class as an alternative to implementing your feature
 * directly in `QuickSuggest`. Doing so has the following advantages:
 *
 * - If your feature is gated on a Nimbus variable or preference, `QuickSuggest`
 *   will manage its lifetime automatically. This is really only useful if the
 *   feature has state that must be initialized when the feature is enabled and
 *   uninitialized when it's disabled.
 *
 * - Encapsulation. You can keep all the code related to your feature in one
 *   place, without mixing it with unrelated code and cluttering up
 *   `QuickSuggest`. You can also test it in isolation from `QuickSuggest`.
 *
 * - Remote settings management. You can register your feature with
 *   `QuickSuggestRemoteSettings` and it will be called at appropriate times to
 *   sync from remote settings.
 *
 * - If your feature also serves suggestions from remote settings, you can
 *   implement one method, `queryRemoteSettings()`, to hook into
 *   `UrlbarProviderQuickSuggest`.
 *
 * - Your feature will automatically get its own logger.
 *
 * To register your subclass with `QuickSuggest`, add it to the `FEATURES` const
 * in QuickSuggest.sys.mjs.
 */
export class BaseFeature {
  /**
   * {boolean}
   *   Whether the feature should be enabled. Typically the subclass will check
   *   the values of one or more Nimbus variables or preferences. `QuickSuggest`
   *   will access this getter only when the quick suggest feature as a whole is
   *   enabled. Otherwise the subclass feature will be disabled automatically.
   */
  get shouldEnable() {
    throw new Error("`shouldEnable` must be overridden");
  }

  /**
   * @returns {Array}
   *   If the subclass's `shouldEnable` implementation depends on any prefs that
   *   are not fallbacks for Nimbus variables, the subclass should override this
   *   getter and return their names in this array so that `update()` can be
   *   called when they change. Names should be relative to `browser.urlbar.`.
   *   It doesn't hurt to include prefs that are fallbacks for Nimbus variables,
   *   it's just not necessary because `QuickSuggest` will update all features
   *   whenever a `urlbar` Nimbus variable or its fallback pref changes.
   */
  get enablingPreferences() {
    return null;
  }

  /**
   * @returns {string}
   *   If the feature manages suggestions served by Merino, the subclass should
   *   override this getter and return the name of the specific Merino provider
   *   that serves them.
   */
  get merinoProvider() {
    return "";
  }

  /**
   * @returns {Array}
   *   If the feature manages one or more types of suggestions served by the
   *   Suggest Rust component, the subclass should override this getter and
   *   return an array of the type names as defined in `suggest.udl`. e.g.,
   *   "Amp", "Wikipedia", "Mdn", etc.
   */
  get rustSuggestionTypes() {
    return [];
  }

  /**
   * This method should initialize or uninitialize any state related to the
   * feature.
   *
   * @param {boolean} _enabled
   *   Whether the feature should be enabled or not.
   */
  enable(_enabled) {}

  /**
   * If the feature manages suggestions from remote settings that should be
   * returned by UrlbarProviderQuickSuggest, the subclass should override this
   * method. It should return remote settings suggestions matching the given
   * search string.
   *
   * @param {string} _searchString
   *   The search string.
   * @returns {Array}
   *   An array of matching suggestions, or null if not implemented.
   */
  async queryRemoteSettings(_searchString) {
    return null;
  }

  /**
   * If the feature manages data in remote settings, the subclass should
   * override this method. It should fetch the data and build whatever data
   * structures are necessary to support the feature.
   *
   * @param {RemoteSettings} _rs
   *   The `RemoteSettings` client object.
   */
  async onRemoteSettingsSync(_rs) {}

  /**
   * If the feature manages suggestions that either aren't served by Merino or
   * whose telemetry type is different from `merinoProvider`, the subclass
   * should override this method. It should return the telemetry type for the
   * given suggestion. A telemetry type uniquely identifies a type of suggestion
   * as well as the kind of `UrlbarResult` instances created from it.
   *
   * @param {object} _suggestion
   *   A suggestion from either remote settings or Merino.
   * @returns {string}
   *   The suggestion's telemetry type.
   */
  getSuggestionTelemetryType(_suggestion) {
    return this.merinoProvider;
  }

  /**
   * If the feature manages one or more suggestion types served by the Suggest
   * Rust component, this method should return true if the given suggestion type
   * is enabled and false otherwise. Many features do nothing but manage a
   * single Rust suggestion type, and the suggestion type should be enabled iff
   * the feature itself is enabled. Those features can rely on the default
   * implementation here since a feature's Rust suggestions will not be fetched
   * if the feature is disabled. Other features either manage multiple
   * suggestion types or have functionality beyond their Rust suggestions and
   * need to remain enabled even when their suggestions are not. Those features
   * should override this method.
   *
   * @param {string} _type
   *   A Rust suggestion type name as defined in `suggest.udl`, e.g., "Amp",
   *   "Wikipedia", "Mdn", etc. See also `BaseFeature.rustSuggestionTypes`.
   * @returns {boolean}
   *   Whether the suggestion type is enabled.
   */
  isRustSuggestionTypeEnabled(_type) {
    return true;
  }

  /**
   * If the feature corresponds to a type of suggestion, the subclass should
   * override this method. It should return a new `UrlbarResult` for a given
   * suggestion, which can come from either remote settings or Merino.
   *
   * @param {UrlbarQueryContext} _queryContext
   *   The query context.
   * @param {object} _suggestion
   *   The suggestion from either remote settings or Merino.
   * @param {string} _searchString
   *   The search string that was used to fetch the suggestion. It may be
   *   different from `queryContext.searchString` due to trimming, lower-casing,
   *   etc. This is included as a param in case it's useful.
   * @returns {UrlbarResult}
   *   A new result for the suggestion.
   */
  async makeResult(_queryContext, _suggestion, _searchString) {
    return null;
  }

  // Methods not designed for overriding below

  /**
   * @returns {Logger}
   *   The feature's logger.
   */
  get logger() {
    if (!this._logger) {
      this._logger = lazy.UrlbarUtils.getLogger({
        prefix: `QuickSuggest.${this.name}`,
      });
    }
    return this._logger;
  }

  /**
   * @returns {boolean}
   *   Whether the feature is enabled. The enabled status is automatically
   *   managed by `QuickSuggest` and subclasses should not override this.
   */
  get isEnabled() {
    return this.#isEnabled;
  }

  /**
   * @returns {string}
   *   The feature's name.
   */
  get name() {
    return this.constructor.name;
  }

  /**
   * Enables or disables the feature according to `shouldEnable` and whether
   * quick suggest is enabled. If the feature's enabled status changes,
   * `enable()` is called with the new status; otherwise `enable()` is not
   * called. If the feature manages any Rust suggestion types that become
   * enabled as a result, they will be ingested.
   */
  update() {
    let enable =
      lazy.UrlbarPrefs.get("quickSuggestEnabled") && this.shouldEnable;
    if (enable != this.isEnabled) {
      this.logger.info(`Setting enabled = ${enable}`);
      this.#isEnabled = enable;
      this.enable(enable);
    }

    lazy.QuickSuggest.rustBackend?.ingestEnabledSuggestions(this);
  }

  #isEnabled = false;
}
