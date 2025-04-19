import { mount } from '@vue/test-utils'
import Login from '@/views/Login.vue'

describe('Login.vue', () => {
    test('рендерит кнопку входа', () => {
        const wrapper = mount(Login)
        expect(wrapper.find('button').text()).toBe('Войти через Яндекс')
    })
})
