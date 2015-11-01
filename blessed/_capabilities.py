"""Terminal capability builder patterns."""
# std imports
import re

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 requires 3rd party library (backport)
    #
    # pylint: disable=import-error
    #         Unable to import 'ordereddict'
    from ordereddict import OrderedDict

__all__ = (
    'CAPABILITY_DATABASE',
    'CAPABILITIES_RAW_MIXIN',
    'CAPABILITIES_ADDITIVES',
    'CAPABILITIES_CAUSE_MOVEMENT',
)

CAPABILITY_DATABASE = OrderedDict((
    ('bell', ('bel', {})),
    ('carriage_return', ('cr', {})),
    ('change_scroll_region', ('csr', {'nparams': 2})),
    ('clear_all_tabs', ('tbc', {})),
    ('clear_screen', ('clear', {})),
    ('clr_bol', ('el1', {})),
    ('clr_eol', ('el', {})),
    ('clr_eos', ('clear_eos', {})),
    ('column_address', ('hpa', {'nparams': 1})),
    ('cursor_address', ('cup', {'nparams': 2})),
    ('cursor_down', ('cud1', {})),
    ('cursor_home', ('home', {})),
    ('cursor_invisible', ('civis', {})),
    ('cursor_left', ('cub1', {})),
    ('cursor_normal', ('cnorm', {})),
    ('cursor_report', ('u6', {'nparams': 2})),
    ('cursor_right', ('cuf1', {})),
    ('cursor_up', ('cuu1', {})),
    ('cursor_visible', ('cvvis', {})),
    ('delete_character', ('dch1', {})),
    ('delete_line', ('dl1', {})),
    ('enter_blink_mode', ('blink', {})),
    ('enter_bold_mode', ('bold', {})),
    ('enter_dim_mode', ('dim', {})),
    ('enter_fullscreen', ('smcup', {})),
    ('enter_standout_mode', ('standout', {})),
    ('enter_superscript_mode', ('superscript', {})),
    ('enter_susimpleript_mode', ('susimpleript', {})),
    ('enter_underline_mode', ('underline', {})),
    ('erase_chars', ('ech', {'nparams': 1})),
    ('exit_alt_charset_mode', ('rmacs', {})),
    ('exit_am_mode', ('rmam', {})),
    ('exit_attribute_mode', ('sgr0', {})),
    ('exit_ca_mode', ('rmcup', {})),
    ('exit_fullscreen', ('rmcup', {})),
    ('exit_insert_mode', ('rmir', {})),
    ('exit_standout_mode', ('rmso', {})),
    ('exit_underline_mode', ('rmul', {})),
    ('flash_hook', ('hook', {})),
    ('flash_screen', ('flash', {})),
    ('insert_line', ('il1', {})),
    ('keypad_local', ('rmkx', {})),
    ('keypad_xmit', ('smkx', {})),
    ('meta_off', ('rmm', {})),
    ('meta_on', ('smm', {})),
    ('orig_pair', ('op', {})),
    ('parm_down_cursor', ('cud', {'nparams': 1})),
    ('parm_left_cursor', ('cub', {'nparams': 1})),
    ('parm_dch', ('dch', {'nparams': 1})),
    ('parm_delete_line', ('dl', {'nparams': 1})),
    ('parm_ich', ('ich', {'nparams': 1})),
    ('parm_index', ('indn', {'nparams': 1})),
    ('parm_insert_line', ('il', {'nparams': 1})),
    ('parm_right_cursor', ('cuf', {'nparams': 1})),
    ('parm_rindex', ('rin', {'nparams': 1})),
    ('parm_up_cursor', ('cuu', {'nparams': 1})),
    ('print_screen', ('mc0', {})),
    ('prtr_off', ('mc4', {})),
    ('prtr_on', ('mc5', {})),
    ('reset_1string', ('r1', {})),
    ('reset_2string', ('r2', {})),
    ('reset_3string', ('r3', {})),
    ('restore_cursor', ('rc', {})),
    ('row_address', ('vpa', {'nparams': 1})),
    ('save_cursor', ('sc', {})),
    ('scroll_forward', ('ind', {})),
    ('scroll_reverse', ('rev', {})),
    ('set0_des_seq', ('s0ds', {})),
    ('set1_des_seq', ('s1ds', {})),
    ('set2_des_seq', ('s2ds', {})),
    ('set3_des_seq', ('s3ds', {})),
    # this 'color' is deceiving, but often matching, and a better match
    # than set_a_attributes1 or set_a_foreground.
    ('color', ('_foreground_color', {'nparams': 1, 'match_any': True,
                                     'numeric': 1})),

    # very likely, this will be the most commonly matched inward attribute.
    ('set_a_attributes1', ('sgr1', {'nparams': 1, 'match_any': True,
                                    'match_optional': True})),
    ('set_a_attributes2', ('sgr1', {'nparams': 2, 'match_any': True})),
    ('set_a_attributes3', ('sgr1', {'nparams': 3, 'match_any': True})),
    ('set_a_attributes4', ('sgr1', {'nparams': 4, 'match_any': True})),
    ('set_a_attributes5', ('sgr1', {'nparams': 5, 'match_any': True})),
    ('set_a_attributes6', ('sgr1', {'nparams': 6, 'match_any': True})),
    ('set_a_attributes7', ('sgr1', {'nparams': 7, 'match_any': True})),
    ('set_a_attributes8', ('sgr1', {'nparams': 8, 'match_any': True})),
    ('set_a_attributes9', ('sgr1', {'nparams': 9, 'match_any': True})),
    ('set_a_foreground', ('color', {'nparams': 1, 'match_any': True,
                                    'numeric': 1})),
    ('set_a_background', ('on_color', {'nparams': 1, 'match_any': True,
                                       'numeric': 1})),
    ('set_tab', ('hts', {})),
    ('tab', ('ht', {})),
))

CAPABILITIES_RAW_MIXIN = {
    'bell': re.escape('\a'),
    'carriage_return': re.escape('\r'),
    'cursor_left': re.escape('\b'),
    'cursor_report': re.escape('\x1b') + r'\[(\d+)\;(\d+)R',
    'cursor_right': re.escape('\x1b') + r'\[C',
    'exit_attribute_mode': re.escape('\x1b') + r'\[m',
    'parm_left_cursor': re.escape('\x1b') + r'\[(\d+)D',
    'parm_right_cursor': re.escape('\x1b') + r'\[(\d+)C',
    'scroll_forward': re.escape('\n'),
    'set0_des_seq': re.escape('\x1b(B'),
    'set_a_attributes1': re.escape('\x1b') + r'\[(\d+)?m',
    'set_a_attributes2': re.escape('\x1b') + r'\[(\d+)\;(\d+)m',
    'set_a_attributes3': re.escape('\x1b') + r'\[(\d+)\;(\d+)\;(\d+)m',
    'set_a_attributes4': re.escape('\x1b') + r'\[(\d+)\;(\d+)\;(\d+)\;(\d+)m',
    'tab': re.escape('\t'),
    # one could get carried away, such as by adding '\x1b#8' (dec tube
    # alignment test) by reversing basic vt52, ansi, and xterm sequence
    # parsers.  There is plans to do just that for ANSI.SYS support.
}

CAPABILITIES_ADDITIVES = {
    'color256': ('color', re.escape('\x1b') + r'\[38;5;(\d+)m'),
    'shift_in': ('', re.escape('\x0f')),
    'shift_out': ('', re.escape('\x0e')),
    # this helps where xterm's sgr0 includes set0_des_seq, we'd
    # rather like to also match this immediate substring.
    'sgr0': ('sgr0', re.escape('\x1b') + r'\[m'),
    'backspace': ('', re.escape('\b')),
    'ascii_tab': ('', re.escape('\t')),
}

CAPABILITIES_CAUSE_MOVEMENT = (
    'ascii_tab',
    'backspace'
    'carriage_return',
    'clear_screen',
    'column_address',
    'cursor_address',
    'cursor_down',
    'cursor_home',
    'cursor_left',
    'cursor_right',
    'cursor_up',
    'enter_fullscreen',
    'exit_fullscreen',
    'parm_down_cursor',
    'parm_left_cursor',
    'parm_right_cursor',
    'parm_up_cursor',
    'restore_cursor',
    'row_address',
    'scroll_forward',
    'tab',
)
