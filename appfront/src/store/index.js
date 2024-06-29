
import Vue from 'vue';  
import Vuex from 'vuex';  
  
Vue.use(Vuex);  
  
export default new Vuex.Store({  
  state: {  
    isLoggedIn: false, // 初始状态，用户未登录  
    // ... 其他状态  
  },  
  mutations: {  
    setLoggedIn(state, isLoggedIn) {  
      state.isLoggedIn = isLoggedIn;  
    },  
    // ... 其他mutations  
  },  
  actions: {  
  },  
  // ... 其他选项，如getters、modules等  
});