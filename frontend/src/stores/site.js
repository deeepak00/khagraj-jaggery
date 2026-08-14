import { defineStore } from 'pinia'
import { ref } from 'vue'
import { settingsApi } from '@/api'

export const useSiteStore = defineStore('site', () => {
  const settings = ref({
    site_name:           'KhagRaj',
    site_tagline:        'Pure Jaggery, Ancient Goodness — An Initiative by Lal Ji Foods',
    site_logo:           '/uploads/logo.png',
    hero_title:          'Pure <em>Jaggery</em>,<br>Ancient Goodness.',
    hero_subtitle:       'Handcrafted in small batches using traditional methods. No chemicals, no additives — just pure, golden sweetness. An initiative by Lal Ji Foods.',
    about_title:         'Made with Tradition, Served with Pride',
    about_text:          'KhagRaj was born from a simple belief — that the sweetness of jaggery should never come at the cost of purity. An initiative by Lal Ji Foods, we source fresh sugarcane from local farms and produce jaggery in open iron vessels the old-fashioned way.',
    contact_phone:       '+91-6394050508, +91-8601982296',
    contact_email:       'khagrajindia2017@gmail.com',
    contact_address:     'KhagRaj Production House, Maharashtra, India',
    working_hours:       'Mon–Sat, 9:00 AM – 6:00 PM',
    whatsapp_number:     '916394050508',
    facebook_url:        '',
    instagram_url:       '',
    announcement_text:   '',
    announcement_active: 'false',
    manager_lalji_name:  'Lal Ji',
    manager_lalji_role:  'Founder & Visionary',
    manager_lalji_bio:   'Dedicating decades to restoring health through pure sugarcane jaggery methods.',
    manager_lalji_photo: '',
    manager_awadhesh_name: 'Mr. Awadhesh Maurya',
    manager_awadhesh_role: 'Co-Director (Operations)',
    manager_awadhesh_bio:  'Overseeing quality control, open iron pan cooking processes, and rural farmer alliances.',
    manager_awadhesh_photo: '',
    manager_arjun_name:  'Mr. Arjun Maurya',
    manager_arjun_role:  'Co-Director (Logistics & Reach)',
    manager_arjun_bio:   'Managing modern delivery pipelines and introducing traditional wellness to urban households.',
    manager_arjun_photo: '',
    branches_info:       '📍 Gorakhpur Highway Branch (Main Production House)\nVaranasi-Gorakhpur Highway, Uttar Pradesh\n\n📍 Lucknow Outlet (Retail & Inquiries)\nLal Ji Foods Plaza, Lucknow, Uttar Pradesh\n\n📍 Noida Hub (Distribution & Support)\nSector 62, Noida, Uttar Pradesh',
    shipping_free_threshold: '500',
    shipping_base_fee:      '50',
    seasonal_discount_percent: '0',
    testimonial_1_name: '', testimonial_1_role: '', testimonial_1_text: '', testimonial_1_photo: '',
    testimonial_2_name: '', testimonial_2_role: '', testimonial_2_text: '', testimonial_2_photo: '',
    testimonial_3_name: '', testimonial_3_role: '', testimonial_3_text: '', testimonial_3_photo: '',
  })


  async function fetchPublic() {
    try {
      const { data } = await settingsApi.public()
      settings.value = { ...settings.value, ...data }
    } catch { /* use defaults */ }
  }

  function get(key, fallback = '') {
    return settings.value[key] ?? fallback
  }

  const announcementActive = () => settings.value.announcement_active === 'true'

  return { settings, fetchPublic, get, announcementActive }
})
