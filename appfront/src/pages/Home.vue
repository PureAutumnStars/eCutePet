<template>
    <div style="background-color: ##FFFEF8;">
        <nav-header :active-index="activeIndex" @select="handleNavSelect"></nav-header>
        <router-view></router-view>
        <nav-footer></nav-footer>
    </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import NavFooter from "@/components/NavFooter";
import NavHeader from "@/components/NavHeader";
export default {
  name:'home',
  data() {
    return{
      activeIndex: 0,
      userID: 114514,
    }
  },
  components:{
    NavFooter,
    NavHeader,
  },
  methods: {
    handleNavSelect(path) {  
      if(path == '/myinfo') {
        this.userID = Cookies.get('user_id');
        if(this.userID) {
          this.$router.push({name: 'myinfo', params:{id: this.userID}});
        }
      }
      else
        this.$router.push(path);

      switch (path) {  
        case '/eshop':  
          this.activeIndex = 1;  
          break;  
        case '/community':  
          this.activeIndex = 2;  
          break;  
        case '/doctor':  
          this.activeIndex = 3;  
          break;  
        case '/doclist':  
          this.activeIndex = 4;  
          break;
          case '/about':  
          this.activeIndex = 5;  
          break;   
        default:  
          this.activeIndex = 0;
          break;  
      }  
    }  
  },
  mounted() {

  },
  created() {

  },
}
</script>

<!-- <style>

</style> -->
