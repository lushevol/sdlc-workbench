import { describe, it, expect } from 'vitest';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { configureAppBridgeTools } from '../src/tools.js';

const EXPECTED_TOOLS = [
  'browser_start',
  'browser_close',
  'browser_set_timeouts',
  'browser_navigate',
  'browser_navigate_back',
  'browser_navigate_forward',
  'browser_refresh',
  'browser_get_page_info',
  'browser_get_page_source',
  'browser_wait_for_text',
  'element_find',
  'element_find_all',
  'element_wait_for',
  'element_click',
  'element_send_keys',
  'element_clear',
  'element_get_text',
  'element_get_attribute',
  'element_get_css_value',
  'element_get_rect',
  'element_get_state',
  'element_upload_file',
  'select_get_options',
  'select_option',
  'script_execute',
  'mouse_hover',
  'mouse_double_click',
  'mouse_right_click',
  'mouse_drag_and_drop',
  'keyboard_press_key',
  'alert_handle',
  'cookie_add',
  'cookie_get',
  'cookie_delete',
  'window_manage',
  'frame_manage',
  'screenshot_capture',
  'element_scan_page',
  'codegen_generate_test',
  'network_list_requests',
  'network_get_request',
  'network_clear_requests',
  'console_list_messages',
  'console_get_message',
  'console_clear_messages',
  'browser_emulate',
  'performance_start_trace',
  'performance_stop_trace'
];

describe('configureAppBridgeTools', () => {
  it('registers every expected tool exactly once', () => {
    const server = createMockServer();
    configureAppBridgeTools(server);

    const registeredNames = server.getRegisteredTools().map((tool) => tool.name);

    for (const name of EXPECTED_TOOLS) {
      expect(registeredNames).toContain(name);
    }
    expect(new Set(registeredNames).size).toBe(registeredNames.length);
    expect(registeredNames).toHaveLength(EXPECTED_TOOLS.length);
  });
});
