from enum import Enum, auto
from ragger.firmware import Firmware
from ragger.navigator import Navigator, NavInsID, NavIns
from typing import Union


class SettingID(Enum):
    VERBOSE_ENS = auto()
    VERBOSE_EIP712 = auto()
    NONCE = auto()
    DEBUG_DATA = auto()


def get_device_settings(firmware: Firmware) -> list[SettingID]:
    if firmware == Firmware.NANOS:
        return [
            SettingID.NONCE,
            SettingID.DEBUG_DATA,
        ]
    return [
        SettingID.VERBOSE_ENS,
        SettingID.VERBOSE_EIP712,
        SettingID.NONCE,
        SettingID.DEBUG_DATA,
    ]


def get_setting_per_page(firmware: Firmware) -> int:
    if firmware == Firmware.STAX:
        return 3
    return 2


def get_setting_position(firmware: Firmware, setting: Union[NavInsID, SettingID]) -> tuple[int, int]:
    settings_per_page = get_setting_per_page(firmware)
    if firmware == Firmware.STAX:
        screen_height = 672  # px
        header_height = 88  # px
        footer_height = 92  # px
        option_offset = 350  # px
    else:
        screen_height = 600  # px
        header_height = 92  # px
        footer_height = 97  # px
        option_offset = 420  # px
    usable_height = screen_height - (header_height + footer_height)
    setting_height = usable_height // settings_per_page
    index_in_page = get_device_settings(firmware).index(SettingID(setting)) % settings_per_page
    return option_offset, header_height + (setting_height * index_in_page) + (setting_height // 2)


def settings_toggle(firmware: Firmware, nav: Navigator, to_toggle: list[SettingID]):
    moves: list[Union[NavIns, NavInsID]] = list()
    settings = get_device_settings(firmware)
    # Assume the app is on the home page
    if firmware.is_nano:
        moves += [NavInsID.RIGHT_CLICK] * 2
        moves += [NavInsID.BOTH_CLICK]
        for setting in settings:
            if setting in to_toggle:
                moves += [NavInsID.BOTH_CLICK]
            moves += [NavInsID.RIGHT_CLICK]
        moves += [NavInsID.BOTH_CLICK]  # Back
    else:
        moves += [NavInsID.USE_CASE_HOME_SETTINGS]
        settings_per_page = get_setting_per_page(firmware)
        for setting in settings:
            setting_idx = settings.index(setting)
            if (setting_idx > 0) and (setting_idx % settings_per_page) == 0:
                moves += [NavInsID.USE_CASE_SETTINGS_NEXT]
            if setting in to_toggle:
                moves += [NavIns(NavInsID.TOUCH, get_setting_position(firmware, setting))]
        moves += [NavInsID.USE_CASE_SETTINGS_MULTI_PAGE_EXIT]
    nav.navigate(moves, screen_change_before_first_instruction=False)
