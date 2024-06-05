import { shallowMount } from '@vue/test-utils'
import LoginIndex  from '@/views/login/index.vue'

describe('LoginIndex.vue', () => {
  it('emits an event with user data when login is successful', async () => {
      const wrapper = shallowMount(LoginIndex)
      const inputUsername = wrapper.find('input[type="text"]')
      const inputPassword = wrapper.find('input[type="password"]')
      await inputUsername.setValue('admin')
      await inputPassword.setValue('123456')
      await wrapper.find('form').trigger('submit.prevent')
      expect(wrapper.emits()).toHaveProperty('login-success')
  })
})

// describe('LoginIndex.vue', () => {
//   it('emits an event with user data when login is successful', async () => {
//     const wrapper = shallowMount(LoginIndex, {
//       data() {
//         return {
//           loginForm: {
//             username: '',
//             password: ''
//           }
//         };
//       }
//     });
//     const inputUsername = wrapper.find('input[name="username"]');
//     const inputPassword = wrapper.find('input[name="password"]');
//     await inputUsername.setValue('admin');
//     await inputPassword.setValue('123456');
//     await wrapper.find('button[type="submit"]').trigger('click');
//     expect(wrapper.emitted('login-success')).toBeTruthy();
//   });
// });