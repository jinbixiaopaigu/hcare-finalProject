import store from '@/store'
import defaultSettings from '@/settings'
import useSettingsStore from '@/store/modules/settings'

/**
 * 动态修改标题
 */
export function useDynamicTitle() {
  const settingsStore = useSettingsStore();
  const title = settingsStore.title || '房颤检测结果';
  
  if (settingsStore.dynamicTitle) {
    if (title && title !== 'undefined' && title !== 'null') {
      document.title = title + ' - ' + defaultSettings.title;
    } else {
      document.title = defaultSettings.title;
    }
  } else {
    document.title = defaultSettings.title;
  }
}