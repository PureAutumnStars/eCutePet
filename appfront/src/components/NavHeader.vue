<template> 
<div>
  <nav class="navbar">  
    <ul class="navbar-list">  
      <div class="navbar-left">
          <li class="navbar-item">  
          <p class="navbar-link" @click="handleSelect('/index')">回到首页</p>  
          </li>  
          <li class="navbar-item">
          <p class="navbar-link" @click="handleSelect('/doctor')">宠物医生在线咨询</p>  
          </li>
      </div>  
      <div class="navbar-right">  
          <div v-if="!isLogin" class="avatar-container">
            <div class="navbar-avatar" @mouseover="navToLogin=true" @mouseout="navToLogin=false" @click="routeLogin">  
              <img :src="defaultAvatar" alt="">
            </div>
            <transition name="fade">
            <div class="login-prompt" v-show="navToLogin">
              <h2 class="login-title">立即登录</h2>  
                <div class="login-features">  
                  <div class="feature-item">  
                    <div class="feature-icon">💬</div>  
                    <div class="feature-text">社区互动</div>  
                  </div>  
                  <div class="feature-item">  
                    <div class="feature-icon">💡</div>  
                    <div class="feature-text">专家问答</div>  
                  </div>  
                </div>  
                <div class="login-features">  
                  <div class="feature-item">  
                    <div class="feature-icon">🛍️</div>  
                    <div class="feature-text">折扣商品</div>  
                  </div>  
                  <div class="feature-item">  
                    <div class="feature-icon">🩺</div>  
                    <div class="feature-text">预约问诊</div>  
                  </div>
                </div>
            </div> 
            </transition> 
          </div>
          <div v-if="isLogin" class="avatar-container" @mouseover="showPersonal=true" @mouseout="showPersonal=false">
            <div class="navbar-avatar">  
              <img :src="userAvatar" alt="" v-show="!showPersonal">
            </div>
            <transition name="fade">
            <div class="Personal" v-show="showPersonal">
              <img :src="userAvatar" alt="" v-show="showPersonal">
              <p style="margin-top: 5px; 
                        font-size: 15px;
                        border-bottom: 1px solid #eeeeee;
                        padding-bottom: 10px;">{{username}}</p>
              <div style="display: flex; 
                          flex-direction: row; 
                          justify-content: space-around;
                          border-bottom: 1px solid #eeeeee;
                          padding-bottom: 3px;">
                <div style="font-size: 13px;">
                  <p style="margin-top: 0px;">{{userPostnum}}</p>
                  <p style="margin-top: -10px; color: #787879;">发帖数</p>
                </div>
                <div style="font-size: 13px;">
                  <p style="margin-top: 0px;">{{userCommentnum}}</p>
                  <p style="margin-top: -10px; color: #787879;">评论数</p>
                </div>
                <div style="font-size: 13px;">
                  <p style="margin-top: 0px;">{{userFavournum}}</p>
                  <p style="margin-top: -10px; color: #787879;">收藏数</p>
                </div>
              </div>
              <div style="border-bottom: 1px solid #eeeeee;
                          padding-bottom: 0px;">
                <p class="routeP" @click="handleSelect('/myinfo')"><i class="el-icon-user-solid"></i>&nbsp;&nbsp;&nbsp;个人中心</p>
                <p class="routeP" @click="handleSelect('/myorder')"><i class="el-icon-s-order"></i>&nbsp;&nbsp;&nbsp;我的订单</p>
                <p class="routeP" @click="handleSelect('/myappoint')"><i class="el-icon-s-management"></i>&nbsp;&nbsp;&nbsp;我的预约</p>
                <p class="routeP" @click="handleSelect('/mypost')"><i class="el-icon-question"></i>&nbsp;&nbsp;&nbsp;我的帖子</p>
                <p class="routeP" @click="handleSelect('/myfavor')"><i class="el-icon-star-on"></i>&nbsp;&nbsp;&nbsp;我的收藏</p>
              </div>
              <p class="routeP" @click="doLogout"><i class="el-icon-back"></i>&nbsp;&nbsp;&nbsp;退出</p>
            </div> 
            </transition> 
          </div>
          <li class="navbar-item"> 
          <p class="navbar-link" @click="goToadmin">平台管理</p>
          </li>  
      </div>  
    </ul>  
  </nav>  

  <nav class="routebar">  
    <div class="routebar-container">  
      <a href="#" class="routebar-logo">  
        <img src='../assets/images/home/navHeader_title.png' alt="Logo">  
      </a>  
      <ul class="custom-menu">  
        <li  
          class="custom-menu-item"  
          :class="{ 'is-active': activeIndex === 1 }"  
          @click="handleSelect('/eshop')"  
        >  
          <a href="#">E购商品库</a>  
        </li>  
        <li  
          class="custom-menu-item"  
          :class="{ 'is-active': activeIndex === 2 }"  
          @click="handleSelect('/community')"  
        >  
          <a href="#">萌宠社区</a>  
        </li>  
        <li  
          class="custom-menu-item"  
          :class="{ 'is-active': activeIndex === 3 }"  
          @click="handleSelect('/doctor')"  
        >  
          <a href="#">问诊预约</a>  
        </li>
      </ul>  
    </div>  
  </nav>  
</div>
</template>  

<script>
import Cookies from "js-cookie";
export default {
  name:'nav-header',
  data() {
    return {
        defaultAvatar: require('../assets/images/logo.png'),
        userAvatar: null,
        navToLogin: false, 
        showPersonal: false,
        isLogin: true,
        username: '',

        userPostnum: 0,
        userCommentnum: 0,
        userFavournum: 0,
    };
  },
  props: ['activeIndex'],
  methods: {
    routeLogin() {  
        this.$router.push({ path: "/login" });
        this.hideTooltip();  
    },  
    handleSelect(path) { 
      this.$emit('select', path);  
    },  
    goToadmin(){
      window.location.href = 'http://182.92.171.51:8000/admin/'
    },
    checkLogin(){
      const token = Cookies.get(`token`);
      if(token) {
        this.isLogin = true;
      }
      else {
        this.isLogin = false;
      }
    },
    doLogout(){
      Cookies.remove('token');
      Cookies.remove('user_id');
      Cookies.remove(`doctor_id`);
      this.$router.push('/index');
      this.checkLogin();
    }
  },
  mounted() {
    
  },
  created() {
    // 检查登录情况
    this.checkLogin();
    // 获取用户头像和用户名 这个信息可能并不是在这里获取的 到时候讨论
    this.userAvatar = require("../assets/images/userAvatar.jpg");
    this.username = '清秋自有梧桐在';

    this.userPostnum = 13;
    this.userCommentnum = 6;
    this.userFavournum = 45
  },
}
</script>

<style scoped>  
.fade-enter-active, .fade-leave-active {  
  transition: opacity .25s;  
}  
.fade-enter, .fade-leave-to {  
  opacity: 0;  
}  
.fade-enter-to, .fade-leave {  
  opacity: 1;  
}

.navbar {  
  background-color: #e55e5e;  
  padding: 10px;  
}  
  
.navbar-list {
    display: flex;
    list-style: none;  
    margin: 0;  
    padding: 0;  
}  
  
.navbar-item {  
  margin-right: 0px; 
}  
  
.navbar-link {  
  color: #fff;  
  text-decoration: none;  
  padding: 5px 10px;  
  display: inline-block;
  cursor: pointer;
  margin-top: 0px;
  margin-bottom: 0px;
}  
  
.navbar-link:hover {  
  background-color: rgba(255, 255, 255, 0.1); 
}  
.navbar-left {  
    display: flex;
}  

.navbar-right {  
    display: flex;
    margin-left: auto;
}  
.avatar-container {  
  position: relative;   
  width: 50px; 
  height: auto;
}  

.Personal {  
  width: 210px;  
  height: 390px;  
  background-color: #FFFEF5;  
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);  
  position: absolute;
  z-index: 10;
  left: -80px;
}  

.Personal img {  
  height: 45px;  
  width: 45px;  
  border-radius: 50%;
  margin-top: -25px;
  overflow: hidden; 
  object-fit: cover;
}  

.routeP{
  user-select: none; 
  -moz-user-select: none; 
  -ms-user-select: none;
  -webkit-user-select: none; 
  text-align: left;
  margin-left: 15px;
  cursor: pointer;
  color: #787879;
}

.routeP:hover{
  color: #EE6F60
}

.navbar-avatar {  
  height: 30px;  
  width: 30px;  
  margin-right: 0px; 
  margin-top: 2px;
  cursor: pointer;
  position: relative;  
  display: inline-block;  
}  
  
.navbar-avatar img {  
  height: 100%;  
  width: 100%;  
  border-radius: 50%;
  overflow: hidden; 
  object-fit: cover;
}  
.login-prompt {    
  background-color: transparent;  
  background-image: url('../assets/images/home/login_tip.png');
  position: absolute;
  top: 100%;
  margin-left: -135px;
  width: 288px; 
  height: 195px;
  padding: 10px; 
  background-size: contain;
  z-index: 10;
}  
.login-prompt[v-show] {  
  opacity: 1;  
  visibility: visible;  
}  
  
.login-title {  
  margin-bottom: 10px;  
  margin-top: 40px;
  color: #f8e9e9;
}  

.login-title {  
  position: relative; 
  margin-bottom: 15px; 
  text-align: center; 
}  

.login-title::after {  
  content: '';
  position: absolute; 
  bottom: -10px;   
  left: 50%; 
  width: 90%; 
  max-width: 240px;   
  height: 1px; 
  background-color: #ff6767; 
  transform: translateX(-50%);  
}

.login-features {  
  display: flex;  
  justify-content: center; 
  margin-bottom: 10px;  
  margin-left: 10px;
}  
  
.feature-item {  
  display: flex;  
  align-items: center;
  margin-right: 20px;
}  
  
.feature-icon {  
  font-size: 24px;
  margin-right: 10px;
}  
  
.feature-text {  
  color: #ffd8d8;
}
.routebar {  
  width: 100%; 
  background: url('../assets/images/home/navHeader_bg.png') no-repeat center center;   
  background-size: cover;  
  height: 124px;
}  
  
.routebar-container {  
  display: flex;  
  justify-content: center;
  align-items: center; 
  padding: 0 20px; 
  max-width: 1200px;  
  margin: 0 auto;  
}  
  
.routebar-logo img {  
  margin-top: 15px;
  height: 75px;
  margin-right: 20px; 
}  
.custom-menu {  
  /* 自定义菜单样式 */  
  display: flex;  
  list-style: none;  
  padding: 0;  
  margin-left: 30px;  
}  
  
.custom-menu-item {   
  position: relative; 
  margin-right: 100px; 
  margin-top: 20px;
  font-size: 26px;
  flex-shrink: 0; 
  text-decoration: none;
}  
  
.custom-menu-item a {  
  text-decoration: none;  
  color: #7A5151; 
  display: inline-block;
  padding-bottom: 10px;   
}  

.custom-menu-item.is-active a {  
  color: #e55e5e;   
}

.custom-menu-item.is-active::after {  
  content: '';  
  position: absolute;  
  left: 0;  
  bottom: 0;  
  width: 100%;  
  height: 4px; 
  background-color: #e55e5e;  
}  
  
.custom-menu-item:hover a {  
  color: #e55e5e;  
}  
  
.custom-menu-item:hover::after {  
  content: '';  
  position: absolute;  
  left: 0;  
  bottom: 0;  
  width: 100%;  
  height: 4px; 
  background-color: #e55e5e; 
} 
</style>