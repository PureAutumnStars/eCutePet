<!-- 
主页 /index 先不管
待完善功能： !!NavHeader.vue有更新!!
    1. create() 轮播图商品id定义 热销商品信息获取
-->

<template>  
<div class="indexWindow">
  <div class="ad-windows">  
    <el-carousel height="400px" trigger="click" :interval="4000">  
      <el-carousel-item v-for="(item, index) in adList" :key="index">  
        <img :src="item.image" class="carousel-image rounded-corners" @click="routeGood(carousel_id)">  
      </el-carousel-item>  
    </el-carousel>  
  </div>  

  <div class="shop-windows">
    <el-button type="primary" class="top-right-button" 
      icon="el-icon-refresh" @click="switchHotgoods ? switchHotgoods=false:switchHotgoods=true">
      <i prefix-icon="el-icon-user"></i>换一批
    </el-button>
    <button class="routebutton" @click="routePage('eshop')"></button>
    <div id="shoplist">
      <ul v-if="!switchHotgoods" v-for="(item,index) in hotGoodlist.slice(0,5)" style="list-style-type: none; margin-left: 0px;">
          <li class="item" @click="routeGood(item.id)">
              <div class="img_box"><img v-bind:src="item.image_url" alt=""></div>
              <h5 v-html="item.title" class="title"></h5> 
              <div class="product-details">
                <span class="hotprice">&yen;{{item.price}}</span>
                <p>{{ item.sold_num }}+人已付款</p>
              </div>
          </li>
      </ul>
      <ul v-if="switchHotgoods" v-for="(item,index) in hotGoodlist.slice(5,10)" style="list-style-type: none; margin-left: 0px;">
          <li class="item" @click="routeGood(item.id)">
              <div class="img_box"><img v-bind:src="item.image_url" alt=""></div>
              <h5 v-html="item.title" class="title"></h5> 
              <div class="product-details">
                <span class="hotprice">&yen;{{item.price}}</span>
                <p>{{ item.sold_num }}+人已付款</p>
              </div>
          </li>
      </ul>
    </div>
  </div>
  
  <img src="../assets/images/home/index/ad_middle.gif" @click="routeGood(carousel_id)" alt="" style="width: 1200px; height: auto; margin-bottom: 20px;"> 
  
  <div class="community-windows">
    <button class="routebutton" @click="routePage('community')"></button>
    <div class="calpost-windows">  
      <el-carousel height="300px" trigger="click" :interval="3000" direction="vertical">  
        <el-carousel-item v-for="(item, index) in postList" :key="index">  
          <img :src="item.image" @click="routePost(special_postid[index])">
          <p class="bottom_tips">{{item.title}}</p> 
        </el-carousel-item>  
      </el-carousel>  
    </div>
    <div class="hotpost-windows">  
      <div class="recommend">
        <h3>推荐阅读</h3>
        <ul v-for="(item,index) in recommend_postlist" :key="index">
            <li>
              <p @click="routePost(item.id)">{{item.title.length<=17 ? item.title:item.title.slice(0,17)+'...'}}</p>
            </li>
        </ul>
      </div>
      <div class="discuss">
        <h3>热门讨论</h3>
        <ul v-for="(item,index) in hotdiscuss_postlist" :key="index">
            <li>
              <p @click="routePost(item.id)">{{item.title.length<=17 ? item.title:item.title.slice(0,17)+'...'}}</p>
            </li>
        </ul>
      </div>
    </div>
  </div>
  <img src="../assets/images/home/index/ad_end.gif" @click="routeGood(carousel_id)" alt="" style="width: 1200px; height: auto; margin-bottom: 30px;"> 
</div>
</template>

<script>
import axios from "axios";
import { getNormList } from "../api/api.js"
export default {
  name:'index',
  data() {
    return {
      adList: [  
        { image: require('../assets/images/home/index/ad_1.gif')},  
        { image: require('../assets/images/home/index/ad_2.gif')},  
        { image: require('../assets/images/home/index/ad_3.gif')},  
      ],
      postList: [
        { image: require('../assets/images/home/index/frontpost1.png'), title: "狗狗皮肤问题频发？警惕湿疹来袭, 及时防治是关键！" },  
        { image: require('../assets/images/home/index/frontpost2.png'), title: "猫咪急性肾炎的症状以及治疗方法" }, 
        { image: require('../assets/images/home/index/frontpost3.png'), title: "狗狗驱虫药怎么选？" }, 
      ],
      switchHotgoods: false,
      hotGoodlist:[],
      recommend_postlist:[],
      hotdiscuss_postlist:[],

      carousel_id: null,
      special_postid: null,
    };
  },
  methods: {
    routeGood(index)
    {
      this.$router.push({name: 'item', params:{id: index}});
    },
    routePost(index)
    {
      this.$router.push({name: 'post', params:{id: index}});
    },
    routePage(path)
    {
      this.$router.push(path);
    }
  },
  mounted() {

  },
  created(){
    //TODO 在这里定义轮播图里 3个普安特商品的id 3个特殊帖子的id
    this.carousel_id = 114514;
    this.special_postid = [19,198,10];

    //TODO index页获取热度商品：后端请求取得10个 此处直接写死
    //
    //
    this.hotGoodlist=[
      {'id': 1, 'title': '辉瑞速诺阿莫西林克拉维酸钾片炎症感染 ','sold_num': 1798, 'price': 49.00, 'image_url': require('../assets/temp/1.jpg')},
      {'id': 2, 'title': '可吉拉非泼罗尼滴剂猫用体外驱虫3支每盒 ','sold_num': 1699, 'price': 98.00, 'image_url': require('../assets/temp/1.jpg')},
      {'id': 3, 'title': '普安特爱滴克非泼罗尼滴剂犬用体外驱虫','sold_num': 1640, 'price': 58.00, 'image_url': require('../assets/temp/1.jpg')},
      {'id': 4, 'title': '普安特普拿杜犬猫通用体内广谱驱虫药','sold_num': 1625, 'price': 38.00, 'image_url': require('../assets/temp/1.jpg')},
      {'id': 5, 'title': '普安特欣尔宁犬猫耳道耳炎耳垢护理药膏','sold_num': 1559, 'price': 29.00, 'image_url': require('../assets/temp/1.jpg')},
      {'id': 6, 'title': '阿莫尔狗狗玩具磨牙耐咬绳结玩具宠物用品 ','sold_num': 994, 'price': 14.99, 'image_url': require('../assets/temp/2.jpg')},
      {'id': 7, 'title': '艾宠仁家2代猫咪零食猫补水均衡营养厂家直销','sold_num': 867, 'price': 50.00, 'image_url': require('../assets/temp/2.jpg')},
      {'id': 8, 'title': '宠物零食冻干桶 冻干猫零食500g鸡肉粒零食','sold_num': 850, 'price': 39.99, 'image_url': require('../assets/temp/2.jpg')},
      {'id': 9, 'title': '大猫日记电动旋转猫玩具自动逗猫棒','sold_num': 823, 'price': 19.99, 'image_url': require('../assets/temp/2.jpg')},
      {'id': 10, 'title': '疯狂的主人猫玩具逗猫棒自嗨解闷神器','sold_num': 654, 'price': 10.00, 'image_url': require('../assets/temp/2.jpg')},
    ];
    
    // TODO index页获取推荐阅读与热门讨论 分别是按favor_num或comment_num排序最高的帖子
    //
    //
    this.recommend_postlist = [
      {"id": "0", "title": "狗狗感冒千万别乱喂药！真的会致命！"},
      {"id": "1", "title": "春季猫咪怎么预防蜱虫？怎么祛除蜱虫春季猫咪怎么预防蜱虫"},
      {"id": "2", "title": "狗狗感冒千万别乱喂药！真的会致命！"},
      {"id": "3", "title": "春季猫咪怎么预防蜱虫？怎么祛除蜱虫"},
      {"id": "4", "title": "狗狗感冒千万别乱喂药！真的会致命！"},
      {"id": "5", "title": "春季猫咪怎么预防蜱虫？怎么祛除蜱虫"},
      {"id": "6", "title": "狗狗感冒千万别乱喂药狗狗感冒千万别乱喂药狗狗感冒千万别乱喂药"},
      {"id": "7", "title": "春季猫咪怎么预防蜱虫？怎么祛除蜱虫"},
    ];

    this.hotdiscuss_postlist = [
      {"id": "8", "title": "春季猫咪怎么预防蜱虫怎么去祛除蜱虫"},
      {"id": "9", "title": "狗狗嘴角发红、肿大是什么问题呢？"},
      {"id": "10", "title": "怎么判断猫是不是得了猫鼻支？"},
      {"id": "11", "title": "狗狗嘴角发红、肿大是什么问题呢？"},
      {"id": "12", "title": "怎么判断猫是不是得了猫鼻支？"},
      {"id": "13", "title": "狗狗嘴角发红、肿大是什么问题呢？"},
      {"id": "14", "title": "怎么判断猫是不是得了猫鼻支？"},
      {"id": "15", "title": "狗狗嘴角发红、肿大是什么问题呢？"},
    ];

  }
}
</script>

<style>
body {  
  background-color: #FFFEF5; /* 你想要的颜色 */  
}
.indexWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.ad-windows{  
  width: 1200px;  
  margin-top: 0px;
  margin-bottom: 30px;
}

.carousel-image {  
  border-radius: 15px;   
}  
  
.rounded-corners {  
  border-radius: 15px;
}  

.shop-windows{
  display: flex;
  position: relative;
  justify-content: space-around; 
  margin-bottom: 30px;
  padding: 0px;
  height: 400px;
  width: 1230px;
  background-image: url("../assets/images/home/index/eshop_bg.png");
}

.top-right-button {  
    position: absolute;
    top: 10px;  
    right: 10px; 
}

.routebutton {  
  position: absolute;
  top: 8px;  
  left: 27px; 
  width: 175px;
  height: 50px;
  background: transparent;
  border-color: transparent;
}

#shoplist {
  width: 1200px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 55px;
  overflow: hidden;
}

.product-details {  
  display: flex;  
  align-items: center;
  margin-bottom: 10px;
  
}  

.product-details p {
  font-size: 12px;
  height: 20px;
  margin-left: 10px;
  margin-top: -5px;
  display: -webkit-box;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: -10px;
}

.hotprice{
  color: red;
  font-size: 21px;
  margin-top: 0px;
  margin-left: 30px;
}

.item {
  border: 1px solid #ccc;
  border-radius: 10px; 
  margin-bottom: 20px; 
  background-color: #fff;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  float: left;
  width: 200px;
  height: 290px;
  margin: 0 5px 10px;
  text-align: center;
  background: #fff;
  margin-right: 20px;
  transition: all 0.25s ease-in-out;
  opacity: 1;
}

.item .img_box {
  width: 180px;
  height: 180px;
  margin: 8px auto;
}

.img_box img {
  border-radius: 10px;
  width: 100%;
  height: 100%;
}

.item h5 {
  font-size: 14px;
  line-height: 20px;
  height: 40px;
  max-width: 180px;
  padding: 0 20px;
  text-align: start;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 5px;
}

.item:hover .title{
  color: #ee6f60
}

.community-windows{
  display: flex;
  justify-content: center;
  position: relative;
  flex-direction: rows; 
  margin-bottom: 10px;
  padding: 0px;
  height: 400px;
  width: 1230px;
  background-image: url("../assets/images/home/index/community_bg.png");
}

.calpost-windows{  
  width: 590px;
  height: 300px;  
  margin-top: 70px;
  margin-left: 10px;
  position: relative;
  margin-right: 0px;
}

.bottom_tips {  
  position: absolute;
  top: 255px;
  left: 10px;
  color: #F1D6A2;
}

.hotpost-windows{  
  width: 590px;  
  margin-top: 50px;
  height: 290px;  
  margin-right: 10px;
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.recommend{
  width: 290px;
  margin-right: 0px;
  font-size: 14px;
  text-align: left;
}

.recommend h3{
  margin-left: 120px;
}

.recommend p:hover{
  color: #F16F60
}

.discuss{
  width: 290px;
  font-size: 14px;
  margin-right: 0px;
  justify-content: center;
  text-align: left;
}

.discuss h3{
  margin-left: 120px;
}

.discuss p:hover{
  color: #F16F60
}

.doctor-windows{
  display: flex;
  position: relative;
  justify-content: space-around; 
  margin-bottom: 30px;
  padding: 0px;
  height: 400px;
  width: 1230px;
  background-image: url("../assets/images/home/index/doctor_bg.png");
}
</style>
