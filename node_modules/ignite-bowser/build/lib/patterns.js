"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Patterns;
(function (Patterns) {
    Patterns["NAV_IMPORTS_SCREENS"] = "} from \"../screens";
    Patterns["NAV_IMPORTS_NAVIGATORS"] = "import[\\s\\S]*from\\s+\"react-navigation\";?";
    Patterns["ROOT_NAV_ROUTES"] = "export const RootNavigator.+[\\s\\S]\\s+{";
    Patterns["NAV_ROUTES"] = "export const [a-zA-Z0-9]+ = create[a-zA-Z]+[(][{]";
})(Patterns = exports.Patterns || (exports.Patterns = {}));
//# sourceMappingURL=patterns.js.map