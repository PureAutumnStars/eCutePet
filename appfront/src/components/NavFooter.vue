<template> 
    <div>
        <div class="footer">
            <div class="footer-logo">
            <img src="../assets/images/logo.png" alt="">
            <h3>E萌宠</h3>
            </div>
            <div class="footer-link">
            <a href="https://www.hit.edu.cn" target="_blank">HIT主页</a><span>|</span>
            <a href="https://cn.vuejs.org/" target="_blank">Vue.js官网</a><span>|</span>
            <a href="https://space.bilibili.com/102597382?spm_id_from=333.1007.0.0" target="_blank">bilibili</a><span>|</span>
            <a href="https://blog.csdn.net/qq_60595239?type=blog" target="_blank">csdn</a>
            </div>
            <div class="copyright">Copyright ©2024 <span class="domain">www.EQpet.com</span> All Rights Reserved.</div>
        </div>
    </div>
</template>

<script>
export default {
  name:'nav-footer',
  data() {
    return {

    };
  },
  methods: {

  },
  mounted() {

  },
  created() {

  },
}
</script>

<style>
.footer{
    height: 234px;
    border-top: 4px solid #FF6600;
    background-color: #e55e5e;
    color: rgb(230, 169, 161);
    font-size: 16px;
    text-align: center;
  .footer-logo{
    margin-top: 20px;
    margin-bottom: 20px;
  }
  img{
    width: 100px;
    height: 100px;
    margin-bottom: -15px;
    margin-left: -10px;
  }
  h3{
      color: rgb(255, 255, 255);
  }
  .footer-link{
    a{
      color: rgb(230, 169, 161);
      display: inline-block;
    }
    span{
      margin: 0 10px;
    }
    margin-bottom: 13px;
  }
  .copyright{
    .domain{
      color: rgb(230, 169, 161);
    }
  }
}
</style>