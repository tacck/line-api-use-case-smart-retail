"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getSchema = exports.attributes = exports.Attribute = void 0;
var __1 = require("..");
var Attribute;
(function (Attribute) {
    Attribute["ACCESS_CAMERA"] = "accessCamera";
    Attribute["CAMERA"] = "camera";
    Attribute["CAMERA_SETTINGS"] = "cameraSettings";
    Attribute["CAMERA_TYPE"] = "cameraType";
    Attribute["CONFIGURE"] = "configure";
    Attribute["ENABLE_CAMERA_SWITCHER"] = "enableCameraSwitcher";
    Attribute["ENABLE_PINCH_TO_ZOOM"] = "enablePinchToZoom";
    Attribute["ENABLE_TAP_TO_FOCUS"] = "enableTapToFocus";
    Attribute["ENABLE_TORCH_TOGGLE"] = "enableTorchToggle";
    Attribute["GUI_STYLE"] = "guiStyle";
    Attribute["LASER_AREA"] = "laserArea";
    Attribute["PLAY_SOUND_ON_SCAN"] = "playSoundOnScan";
    Attribute["SCANNING_PAUSED"] = "scanningPaused";
    Attribute["SINGLE_IMAGE_MODE_SETTINGS"] = "singleImageModeSettings";
    Attribute["TARGET_SCANNING_FPS"] = "targetScanningFPS";
    Attribute["VIBRATE_ON_SCAN"] = "vibrateOnScan";
    Attribute["VIDEO_FIT"] = "videoFit";
    Attribute["VIEWFINDER_AREA"] = "viewfinderArea";
    Attribute["VISIBLE"] = "visible";
    Attribute["CONFIGURE_ENGINE_LOCATION"] = "configure.engineLocation";
    Attribute["CONFIGURE_LICENSE_KEY"] = "configure.licenseKey";
    Attribute["CONFIGURE_PRELOAD_ENGINE"] = "configure.preloadEngine";
    Attribute["CONFIGURE_PRELOAD_BLURRY_RECOGNITION"] = "configure.preloadBlurryRecognition";
    Attribute["SCAN_SETTINGS_BLURRY_RECOGNITION"] = "scanSettings.blurryRecognition";
    Attribute["SCAN_SETTINGS_CODE_DIRECTION_HINT"] = "scanSettings.codeDirectionHint";
    Attribute["SCAN_SETTINGS_CODE_DUPLICATE_FILTER"] = "scanSettings.codeDuplicateFilter";
    Attribute["SCAN_SETTINGS_ENABLED_SYMBOLOGIES"] = "scanSettings.enabledSymbologies";
    Attribute["SCAN_SETTINGS_GPU_ACCELERATION"] = "scanSettings.gpuAcceleration";
    Attribute["SCAN_SETTINGS_MAX_NUMBER_OF_CODES_PER_FRAME"] = "scanSettings.maxNumberOfCodesPerFrame";
    Attribute["SCAN_SETTINGS_SEARCH_AREA"] = "scanSettings.searchArea";
})(Attribute = exports.Attribute || (exports.Attribute = {}));
exports.attributes = Object.values(Attribute);
var schema;
// tslint:disable-next-line: max-func-body-length
function getSchema() {
    var _a;
    if (schema != null) {
        return schema;
    }
    return (schema = Object.freeze((_a = {},
        // tslint:disable-next-line: no-unnecessary-class
        _a[Attribute.ACCESS_CAMERA] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.CAMERA] = {
            type: "camera",
            default: undefined,
        },
        _a[Attribute.CAMERA_SETTINGS] = {
            type: "cameraSettings",
            default: undefined,
        },
        _a[Attribute.CAMERA_TYPE] = {
            type: "cameraType",
            default: __1.Camera.Type.BACK,
        },
        _a[Attribute.CONFIGURE] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.ENABLE_CAMERA_SWITCHER] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.ENABLE_PINCH_TO_ZOOM] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.ENABLE_TAP_TO_FOCUS] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.ENABLE_TORCH_TOGGLE] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.GUI_STYLE] = {
            type: "guiStyle",
            default: __1.BarcodePicker.GuiStyle.LASER,
        },
        _a[Attribute.LASER_AREA] = {
            type: "searchArea",
            default: undefined,
        },
        _a[Attribute.PLAY_SOUND_ON_SCAN] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.SCANNING_PAUSED] = {
            type: "boolean",
            default: false,
        },
        _a[Attribute.SINGLE_IMAGE_MODE_SETTINGS] = {
            type: "singleImageModeSettings",
            default: undefined,
        },
        _a[Attribute.TARGET_SCANNING_FPS] = {
            type: "integer",
            default: 30,
        },
        _a[Attribute.VIBRATE_ON_SCAN] = {
            type: "boolean",
            default: false,
        },
        _a[Attribute.VIDEO_FIT] = {
            type: "videoFit",
            default: __1.BarcodePicker.ObjectFit.CONTAIN,
        },
        _a[Attribute.VIEWFINDER_AREA] = {
            type: "searchArea",
            default: undefined,
        },
        _a[Attribute.VISIBLE] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.CONFIGURE_ENGINE_LOCATION] = {
            type: "string",
            default: "/",
        },
        _a[Attribute.CONFIGURE_LICENSE_KEY] = {
            type: "string",
            default: "",
        },
        _a[Attribute.CONFIGURE_PRELOAD_ENGINE] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.CONFIGURE_PRELOAD_BLURRY_RECOGNITION] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.SCAN_SETTINGS_BLURRY_RECOGNITION] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.SCAN_SETTINGS_CODE_DIRECTION_HINT] = {
            type: "codeDirection",
            default: __1.ScanSettings.CodeDirection.LEFT_TO_RIGHT,
        },
        _a[Attribute.SCAN_SETTINGS_CODE_DUPLICATE_FILTER] = {
            type: "integer",
            default: 0,
        },
        _a[Attribute.SCAN_SETTINGS_ENABLED_SYMBOLOGIES] = {
            type: "array",
            default: [],
        },
        _a[Attribute.SCAN_SETTINGS_GPU_ACCELERATION] = {
            type: "boolean",
            default: true,
        },
        _a[Attribute.SCAN_SETTINGS_MAX_NUMBER_OF_CODES_PER_FRAME] = {
            type: "integer",
            default: 1,
        },
        _a[Attribute.SCAN_SETTINGS_SEARCH_AREA] = {
            type: "searchArea",
            default: undefined,
        },
        _a)));
}
exports.getSchema = getSchema;
//# sourceMappingURL=schema.js.map