"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var ramda_1 = require("ramda");
// the default React Native version for this boilerplate
exports.REACT_NATIVE_VERSION = "0.61.2";
// where the version lives under gluegun
var pathToVersion = ["parameters", "options", "react-native-version"];
// accepts the context and returns back the version
var getVersionFromContext = ramda_1.pathOr(exports.REACT_NATIVE_VERSION, pathToVersion);
/**
 * Gets the React Native version to use.
 *
 * Attempts to read it from the command line, and if not there, falls back
 * to the version we want for this boilerplate.  For example:
 *
 *   $ ignite new Custom --react-native-version 0.61.2
 *
 * @param {*} context - The gluegun context.
 */
exports.getReactNativeVersion = function (context) {
    var version = getVersionFromContext(context || {});
    return ramda_1.is(String, version) ? version : exports.REACT_NATIVE_VERSION;
};
//# sourceMappingURL=react-native-version.js.map