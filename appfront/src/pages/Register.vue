<!-- 
注册页面 /register
login点击`去注册`进入
待完善功能：
    1. 普通用户注册 报错分析和输出
    2. 医生用户注册 报错分析和输出
    3. 验证码发送功能
-->

<template>
<div class="login clearfix">
    <div class="login-wrap">
    <el-row type="flex" justify="end">
        <el-col :span="1">  
        </el-col>
        <el-col :span="8">  
            <div class="moduleImg" :style="backgroundStyle" @click="(isMaster && isReady)? switch2D():switch2M()"></div>
        </el-col>  
        <el-col :span="15"> 

        <el-form v-if="!isReady || (isReady && isMaster)" class="regisRec" ref="loginForm" :model="user" status-icon label-width="80px">
        <h3>创建你的账户</h3>
        <hr>
        <el-form-item id="username" prop="username">
            <el-input v-if="!focused_user" @focus="focused_user = true" v-model="user.username" placeholder="用户名" prefix-icon="el-icon-user" maxlength="40"></el-input>
            <el-input v-else @blur="focused_user = false" v-model="user.username" placeholder="" prefix-icon="el-icon-user" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_user ? 1:0, top: focused_user ? '-30px':'0px'}">用户名</span>
        </el-form-item>
        <el-form-item id="email" prop="email">
            <el-input v-if="!focused_email" @focus="focused_email = true" v-model="user.email" placeholder="邮箱" prefix-icon="el-icon-message" maxlength="40"></el-input>
            <el-input v-else @blur="focused_email = false" v-model="user.email" placeholder="" prefix-icon="el-icon-message" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_email ? 1:0, top: focused_email ? '-30px':'0px'}">邮箱</span>
        </el-form-item>
        <el-form-item id="password" prop="password">
            <el-input v-if="!focused_passwd" @focus="focused_passwd = true" v-model="user.password" show-password placeholder="密码" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <el-input v-else @blur="focused_passwd = false" v-model="user.password" show-password placeholder="" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_passwd ? 1:0, top: focused_passwd ? '-30px':'0px'}">密码</span>
        </el-form-item>
        <el-form-item id="repassword" prop="repassword">
            <el-input v-if="!focused_repasswd" @focus="focused_repasswd = true" v-model="user.repass" show-password placeholder="确认密码" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <el-input v-else @blur="focused_repasswd = false" v-model="user.repass" show-password placeholder="" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_repasswd ? 1:0, top: focused_repasswd ? '-30px':'0px'}">确认密码</span>
        </el-form-item>
        <el-form-item id="verify" prop="verify">
            <div class="verify" style="display: flex;">
                <el-input v-if="!focused_verify" 
                    @focus="focused_verify = true" 
                    v-model="user.vericode" placeholder="验证码" 
                    prefix-icon="el-icon-key" 
                    maxlength="40"
                    style="width: 280px;"
                ></el-input>
                <el-input v-else @blur="focused_verify = false" 
                    v-model="user.vericode" 
                    placeholder="" 
                    prefix-icon="el-icon-key" 
                    maxlength="40"
                    style="width: 280px;"
                ></el-input>
                <span class="label" :style="{opacity: focused_verify ? 1:0, top: focused_verify ? '-30px':'0px'}">验证码</span>
                <el-button type="primary" 
                    @click="sendVerifyCode" 
                    :disabled="isSending"
                    style="width: 150px;
                    color: rgb(52, 153, 52); 
                    margin-left: 10px; 
                    margin-top: 1px; 
                    height: 40px;
                    background-color: #ffffff;
                    border-color: #ffffff;
                    font-size: 17px;"
                >{{!isSending? '获取验证码' : countdown+'s'}}</el-button>
            </div>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" style="margin-top: 20px; background-color: #e55e5e; border-color: #e55e5e" @click="doNormRegister()">注册账号</el-button>
        </el-form-item>
        </el-form>

        <el-form v-if="!isMaster && isReady" class="regisRec" ref="loginForm" :model="user" status-icon label-width="80px">
        <h3>创建你的账户</h3>
        <hr>
        <el-form-item id="username" prop="username">
            <el-input v-if="!focused_user" @focus="focused_user = true" v-model="user.username" placeholder="用户名" prefix-icon="el-icon-user" maxlength="40"></el-input>
            <el-input v-else @blur="focused_user = false" v-model="user.username" placeholder="" prefix-icon="el-icon-user" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_user ? 1:0, top: focused_user ? '-30px':'0px'}">用户名</span>
        </el-form-item>
        <el-form-item id="name" prop="name">
            <el-input v-if="!focused_name" @focus="focused_name = true" v-model="user.name" placeholder="姓名" prefix-icon="el-icon-user-solid" maxlength="10"></el-input>
            <el-input v-else @blur="focused_name = false" v-model="user.name" placeholder="" prefix-icon="el-icon-user-solid" maxlength="10"></el-input>
            <span class="label" :style="{opacity: focused_name ? 1:0, top: focused_name ? '-30px':'0px'}">姓名</span>
        </el-form-item>
        <el-form-item id="identity" prop="identity">
            <el-input v-if="!focused_identity" @focus="focused_identity = true" v-model="user.id" placeholder="身份证号" prefix-icon="el-icon-postcard" maxlength="18"></el-input>
            <el-input v-else @blur="focused_identity = false" v-model="user.id" placeholder="" prefix-icon="el-icon-postcard" maxlength="18"></el-input>
            <span class="label" :style="{opacity: focused_identity ? 1:0, top: focused_identity ? '-30px':'0px'}">身份证号</span>
        </el-form-item>
        <el-form-item id="email" prop="email">
            <el-input v-if="!focused_email" @focus="focused_email = true" v-model="user.email" placeholder="邮箱" prefix-icon="el-icon-message" maxlength="40"></el-input>
            <el-input v-else @blur="focused_email = false" v-model="user.email" placeholder="" prefix-icon="el-icon-message" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_email ? 1:0, top: focused_email ? '-30px':'0px'}">邮箱</span>
        </el-form-item>
        <el-form-item id="password" prop="password">
            <el-input v-if="!focused_passwd" @focus="focused_passwd = true" v-model="user.password" show-password placeholder="密码" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <el-input v-else @blur="focused_passwd = false" v-model="user.password" show-password placeholder="" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_passwd ? 1:0, top: focused_passwd ? '-30px':'0px'}">密码</span>
        </el-form-item>
        <el-form-item id="repassword" prop="repassword">
            <el-input v-if="!focused_repasswd" @focus="focused_repasswd = true" v-model="user.repass" show-password placeholder="确认密码" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <el-input v-else @blur="focused_repasswd = false" v-model="user.repass" show-password placeholder="" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_repasswd ? 1:0, top: focused_repasswd ? '-30px':'0px'}">确认密码</span>
        </el-form-item>
        <el-form-item id="post" prop="post">
            <el-input v-if="!focused_post" @focus="focused_post = true" v-model="user.post" placeholder="执业编号" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <el-input v-else @blur="focused_post = false" v-model="user.post" placeholder="" prefix-icon="el-icon-lock" maxlength="40"></el-input>
            <span class="label" :style="{opacity: focused_post ? 1:0, top: focused_post ? '-30px':'0px'}">执业编号</span>
        </el-form-item>
        <el-form-item id="verify" prop="verify">
            <div class="verify" style="display: flex;">
                <el-input v-if="!focused_verify" 
                    @focus="focused_verify = true" 
                    v-model="user.vericode" placeholder="验证码" 
                    prefix-icon="el-icon-key" 
                    maxlength="40"
                    style="width: 280px;"
                ></el-input>
                <el-input v-else @blur="focused_verify = false" 
                    v-model="user.vericode" 
                    placeholder="" 
                    prefix-icon="el-icon-key" 
                    maxlength="40"
                    style="width: 280px;"
                ></el-input>
                <span class="label" :style="{opacity: focused_verify ? 1:0, top: focused_verify ? '-30px':'0px'}">验证码</span>
                <el-button type="primary" 
                    @click="sendVerifyCode" 
                    :disabled="isSending"
                    style="width: 150px;
                    color: rgb(52, 153, 52); 
                    margin-left: 10px; 
                    margin-top: 1px; 
                    height: 40px;
                    background-color: #ffffff;
                    border-color: #ffffff;
                    font-size: 17px;"
                >{{!isSending? '获取验证码' : countdown+'s'}}</el-button>
            </div>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" style="margin-top: 20px; background-color: #e55e5e; border-color: #e55e5e;" @click="doDocRegister()">注册账号</el-button>
        </el-form-item>
        </el-form>

        </el-col>
    </el-row>
    </div>
</div>
</template>

<script>
import axios from "axios";
import { verifyEmail, normRegister , DocRegister } from "../api/api";
export default {
name: "register",
data() {
    return {
    // 用户输入
    user: 
    {
        username: "",  //用户名
        email: "",     //邮箱
        password: "",  //密码
        repass: "",    //确认密码
        vericode: "",  //验证码
        name: "",      //实名（医生）
        id: "",        //身份证号（医生）
        post: "",      //执业编号（医生）
        
    },

    // 用于输出框聚焦动画的变量，可忽略
    focused_user: false,
    focused_passwd: false,
    focused_repasswd: false,
    focused_email: false,
    focused_identity: false,
    focused_name: false,
    focused_post: false,
    focused_verify: false,

    // 用于用户身份提示图切换动画
    moduleUrl: require("../assets/images/login&register/basic.png"),
    isMaster: true,
    isReady: false,

    // 用于验证码按钮和倒计时
    isSending: false,
    sendCooldown: null,
    countdown: 60,

    };
},

// 计算属性
computed: {
    // 用于用户身份提示图切换动画
    backgroundStyle() 
    {  
        return {  backgroundImage: `url(${this.moduleUrl})`,  }
    },

},

// 挂载
mounted() {  
    //用于实现左侧从登录图切换到用户身份图，主要是计时器。如何设计向此处添加内容，考虑下如何合并，不要影响此处功能（？
    setTimeout(() => {
        this.moduleUrl = require("../assets/images/login&register/master.png")
    }, 200) 
    this.isReady = true

},

created() {
},

methods: {
    // 普通用户注册
    doNormRegister() 
    {
        if(!this.user.email) {
            this.$message.error("邮箱为空！");
            return;
        }
        else if(this.user.repass !== this.user.password) {
            this.$message.error("两次输入的密码不一致！");
            return;
        }
        else if(!this.user.vericode) {
            this.$message.error("验证码为空！");
            return;
        }
        normRegister(this.user.username, 
                     this.user.email, 
                     this.user.password,
                     this.user.vericode).then
            (respond =>
                {
                    if(respond.status === 201) {
                        this.$message({
                            message: `注册成功! 欢迎${this.user.username}和您的爱宠加入我们!`,
                            type: 'success'
                        });
                        this.$router.push({ path: "/login" });
                    }
                }
            ).catch
            (error => 
                {
                    if(error.response) {
                        if(error.response.status === 400) {
                            this.$message.error(`${error.response.data}`);
                            return;
                        }
                    }
                    console.error('Request failed:', error);  
                        this.$message.error("注册失败！请检查输入的信息或网络连接情况"); 
                }
            );
    },

    // 医生注册
    doDocRegister() {
        if(!this.user.email) {
            this.$message.error("邮箱为空！");
            return;
        }
        else if(this.user.repass !== this.user.password) {
            this.$message.error("两次输入的密码不一致！");
            return;
        }
        else if(!this.user.vericode) {
            this.$message.error("验证码为空！");
            return;
        }
        else if(!this.user.name || !this.user.id || !this.user.post) {
            this.$message.error("身份验证信息不完整！");
            return;
        }
        DocRegister(this.user.username, 
                    this.user.email, 
                    this.user.password,
                    this.user.id, 
                    this.user.name, 
                    this.user.post,
                    this.user.vericode).then
            (respond =>
                {
                    if(respond.status === 201){
                        this.$message({
                            message: `注册成功! 您的认证申请已经提交, 请关注平台消息！`,
                            type: 'success'
                        });
                        this.$router.push({ path: "/login" });
                    }
        }).catch
        (error =>
            {
                if(error.response) {
                    if(error.response.status === 400) {
                        this.$message.error(`${error.response.data}`);
                        return;
                    }
                }
                console.error('Request failed:', error);  
                this.$message.error("注册失败！请检查输入的信息或网络连接情况"); 
            });

    },

    // 用于切换宠物主和医生身份图
    switch2M(){
        this.isMaster= !this.isMaster;
        this.moduleUrl = require("../assets/images/login&register/master.png");
        setTimeout(() => {}, 1000);
    },
    switch2D(){
        this.isMaster= !this.isMaster;
        this.moduleUrl = require("../assets/images/login&register/doctor.png");
        setTimeout(() => {}, 1000);
    },

    //用于验证码倒计时
    sendVerifyCode(){
        if(this.isSending) return;

        this.isSending = true;
        this.countdown = 60;

        // TODO:
        // 发送邮箱到后端，使后端能发送验证码到用户邮箱等
        //  大概是需要后端的一个API接口，接收参数为user_email，并通过管理员邮箱发生验证码（update：2024/6/17）
        verifyEmail(this.user.email).then(
            respond => {
                if(respond.status === 200) {
                    this.$message(`已经成功向您的邮箱：${this.user.email} 发送验证码，请查收！`);
                }
            }
        ).catch
        (error => {
            if(error.response) {
                if(error.response.status === 422) {
                    this.$message.error("输入的邮箱不合法，请重新输入！");
                    return;
                }
            }
            console.error('Request failed:', error);  
            this.$message.error("验证码发送失败！请检查输入的邮箱或网络连接情况！");
        });
        const intervalId = setInterval(() => {  
        if (this.countdown > 0) {  
          this.countdown--;  
        } else {  
          clearInterval(intervalId);  
          this.isSending = false;  
          this.countdown = 60;
        }  
      }, 1000);
    },

    //看起来没用但是文心一言说有用的东西
    beforeDestroy() {  
      if (this.intervalId) {  
        clearInterval(this.intervalId);  
        this.intervalId = null;  
      }  
    },  
}
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {  
  transition: opacity 0.25s ease-out;  
}  
.fade-enter, .fade-leave-to {  
  opacity: 0;  
}  
.login::before{
content:"";
background-image: url("../assets/images/login&register/basic_bg.jpg"), linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7));
background-blend-mode: overlay;
/* background-image: url("../assets/images/bg1.jpg"); */
mix-blend-mode: multiply;
opacity:1;
z-index:-1;
background-size:100% 100%;
background-attachment:fixed;
width: 100%;
height: 100%;
position: fixed;
top:0px;
left:0px;
}
.login {
margin: 0px;
width: 100%;
height: 100%;
}
.login-wrap {
background: url("../assets/images/login&register/basic_rect.png") no-repeat;
background-size: cover;
width: 800px;
height: 450px;
margin: 250px auto;
overflow: hidden;
padding-top: 10px;
line-height: 80px;
font-size: 20px;
}
.label{
    position: absolute;
    /* top: -30px;
    left: 5px; */
    top: 0px;
    left: 5px;
    color: #000000;
    transition: 0.25s ease-out;
    opacity: 0;
    font-size: small;
}
.moduleImg{
    width: 283px;
    height: 474px;
    background-size: cover;
    background-repeat: no-repeat;
    transition: 0.25s ease-in-out;
}
.regisRec{
    height: 470px;
    overflow-y: auto;
}

.regisRec::-webkit-scrollbar{
    display: none;
}

#username {
width: 440px; 
margin-bottom: 20px;
}
#email {
width: 440px;
margin-bottom: 20px;
margin-right: 60px;
}
#password {
width: 440px;
margin-bottom: 20px;
margin-right: 60px;
}
#repassword {
width: 440px;
margin-bottom: 20px;
margin-right: 60px;
}
#name {
width: 440px;
margin-bottom: 20px;
margin-right: 60px;
}
#identity {
width: 440px;
margin-bottom: 20px;
margin-right: 60px;
}
#post {
width: 440px;
margin-bottom: 20px;
margin-right: 60px;
}
#verify {
width: 495px;
margin-bottom: 20px;
margin-right: 60px;
}
h3 {
color: #e55e5e;
font-size: 30px;
margin-right: 0px;
margin-bottom: 0px;
}
hr {
background-color: #444;
margin: 5px auto 30px;
width: 400px;
}
.el-button {
width: 80%;
margin-right: 55px;
margin-top: -20px;
color: #ffffff;
font-size: large;
}
</style>