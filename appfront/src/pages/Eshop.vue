<!-- 
商城 /eshop
待完善功能：
    1. 新品/热销的查询和维护  //Update Time: 2024/06/25
-->

<template>
  <div class="eshopWindow">
    <div class="titlecontent">
      <el-input placeholder="搜索你感兴趣的商品"
          prefix-icon = "el-icon-search"
          style="display: inline-block;
                width: 900px;
                margin-right: 15px;" 
          v-model="keyWord" clearable></el-input>
      <el-button type="primary" @click='searchList' class="shopButton" 
        style="background-color: #e55e5e;
              border-color: #e55e5e;">搜索</el-button>
    </div>
    <div class="show">
      <div class="label-selector-container">
        <div class="labelSelector">
          <h5 class="labelH">按标签分类</h5>
          <el-checkbox v-model="category.petSnacks" @change="labelChange('petSnacks', $event)">宠物零食</el-checkbox>  
          <div class="secondLabel">  
            <el-checkbox v-model="category.catSnacks" @change="labelChange('catSnacks', $event)">猫咪</el-checkbox>  
            <el-checkbox v-model="category.dogSnacks" @change="labelChange('dogSnacks', $event)">狗狗</el-checkbox>  
            <el-checkbox v-model="category.mouSnacks" @change="labelChange('mouSnacks', $event)">仓鼠</el-checkbox>  
            <el-checkbox v-model="category.rabSnacks" @change="labelChange('rabSnacks', $event)">兔子</el-checkbox>  
          </div>  
        
          <el-checkbox v-model="category.petToys" @change="labelChange('petToys', $event)">宠物玩具</el-checkbox>  
          <div class="secondLabel">  
            <el-checkbox v-model="category.catToys" @change="labelChange('catToys', $event)">猫咪</el-checkbox>  
            <el-checkbox v-model="category.dogToys" @change="labelChange('dogToys', $event)">狗狗</el-checkbox>  
            <el-checkbox v-model="category.mouToys" @change="labelChange('mouToys', $event)">仓鼠</el-checkbox>  
            <el-checkbox v-model="category.rabToys" @change="labelChange('rabToys', $event)">兔子</el-checkbox>  
          </div>  
        
          <el-checkbox v-model="category.petMedic" @change="labelChange('petMedic', $event)">宠物药品</el-checkbox>  
          <div class="secondLabel">  
            <el-checkbox v-model="category.catMedic" @change="labelChange('catMedic', $event)">猫咪</el-checkbox>  
            <el-checkbox v-model="category.dogMedic" @change="labelChange('dogMedic', $event)">狗狗</el-checkbox>  
            <el-checkbox v-model="category.mouMedic" @change="labelChange('mouMedic', $event)">仓鼠</el-checkbox>  
            <el-checkbox v-model="category.rabMedic" @change="labelChange('rabMedic', $event)">兔子</el-checkbox>  
          </div> 
          <h5 class="orderH">排序</h5> 
            <div class="orderSelector">
              <div class="orderItem" @click="order.Time=!order.Time; order.TARGET='Time'; orderList('Time', order.Time);">
                <p v-if="!(order.TARGET==='Time')" style="color: black;">上架时间</p>
                <p v-else-if="order.Time" style="color: #e55e5e; font-weight: bold;">上架时间↑</p>
                <p v-else style="color: #e55e5e; font-weight: bold;">上架时间↓</p>
              </div>
              <div class="orderItem" @click="order.Sold=!order.Sold; order.TARGET='Sold'; orderList('Sold', order.Sold);">
                <p v-if="!(order.TARGET==='Sold')" style="color: black;">销量</p>
                <p v-else-if="order.Sold" style="color: #e55e5e; font-weight: bold;">销量↑</p>
                <p v-else style="color: #e55e5e; font-weight: bold;">销量↓</p>
              </div>
              <div class="orderItem" @click="order.Price=!order.Price; order.TARGET='Price'; orderList('Price', order.Price);">
                <p v-if="!(order.TARGET==='Price')" style="color: black;">价格</p>
                <p v-else-if="order.Price" style="color: #e55e5e; font-weight: bold;">价格↑</p>
                <p v-else style="color: #e55e5e; font-weight: bold;">价格↓</p>
              </div>
            </div>  
        </div>  
      </div>

      <div class="shop-windows">
        <div id="shoplist">
          <ul v-for="(item,index) in paginatedGoods" :key="index" style="list-style-type: none; margin-left: 0px;">
              <li class="item" @click="routeGood(item)">
                  <div class="img_box"><img v-bind:src="item.front_image" alt=""></div>
                  <h5 v-html="item.name" class="title"></h5> 
                  <div class="product-details">
                    <span class="hotprice">&yen;{{item.price}}</span>
                    <p>已卖出{{ item.sold_num }}+件</p>
                  </div>
              </li>
          </ul>
        </div>
        <div class="pagination">  
          <el-pagination  
            @size-change="handleSizeChange"  
            @current-change="handleCurrentChange"  
            :current-page="currentPage"  
            :page-sizes="[15]"  
            :page-size="pageSize"  
            layout="total, sizes, prev, pager, next, jumper"  
            :total="totalGoods">  
          </el-pagination>  
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import { getGoodList } from "../api/api"
export default {
  name:'eshop',
  data() {
    return {
      // 搜索框输入的关键词
      keyWord: '',

      // 获取的待展示商品列表
      Goodlist: [],

      // 当前页面， 每页大小（固定，用于请求时做参数）以及商品数量
      currentPage: 1, 
      pageSize: 15, 
      totalGoods: 0, 

      //标签分类 标志变量
      category: {
        'petSnacks': false,
        'catSnacks': false,
        'dogSnacks': false,
        'mouSnacks': false,
        'rabSnacks': false,
        'petToys': false,
        'catToys': false,
        'dogToys': false,
        'mouToys': false,
        'rabToys': false,
        'petMedic': false,
        'catMedic': false,
        'dogMedic': false,
        'mouMedic': false,
        'rabMedic': false,
      },

      // 排序为正序(true)还是倒序(false), 当前按哪个属性排序(TARGET)
      order: {
        'Time': true,
        'Sold': true,
        'Price': true,
        'TARGET': 'Time',
      },

      //根据搜索框、排序、标签分类得到的查询约束，每次执行executeSearch方法都根据此变量来进行
      last_constraint: {
        category: null, // 根据名判断标签是几级的 变量.slice(0, 3) 字符串
        order: 'Time',
        searchkey: null,
        // 一个排序字段，标志正序/逆序
        if_forward: true
      }
    };
  },

  computed: {  
    // 计算商品切片分页，可忽略
    paginatedGoods() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.Goodlist.slice(start, end);  
    },  
  },

  methods: {
    // 处理页面大小和页码的函数，可忽略
    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },

    // 对于当前的请求约束last_constraint执行一次获取商品列表的请求
    executeSearch()
    {
      this.currentPage = 1;
      const keyword = this.last_constraint.searchkey;
      let self_category = null;
      let parent_category = null;
      const is_hot = false;
      const is_new = false;
      let ordering = 'create_time,sold_num,price';
      if(this.last_constraint.category) {
        if(this.last_constraint.category.slice(0, 3) === 'pet') {
          parent_category = this.last_constraint.category;
        }
        else {
          self_category = this.last_constraint.category;
        }
      }
      if(this.last_constraint.order === 'Time') {
        ordering = 'create_time,sold_num,price';
      }
      else if(this.last_constraint.order === 'Sold') {
        ordering = 'sold_num,creat_time,price';
      }
      else if(this.last_constraint.order === 'Price') {
        ordering = 'price,sold_num,create_time';
      }
      if(this.last_constraint.if_forward === false) {
        ordering = '-' + ordering;
      }
      // ↓
      // Todo：维护 is_hot 和 is_new 的部分，这两个参数在iter4中并未用到
      // ↑
      getGoodList(keyword, self_category, parent_category, is_hot, is_new, ordering, 1, 199).then
      (response => 
        {
          if(response.status === 200) {
            this.Goodlist = response.data.results;
            this.totalGoods = response.data.count;
            // for debug
            // this.$message(`查询成功，返回结果如本页所示，当前商城内共有满足该需求的商品 ${this.totalGoods} 个`);
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询失败，请检查网络状况！');
        }
      )
    },

    // 按标签分类功能 labelName:当前选择的标签 newValue:选中labelName标签时为真, 取消labelName标签为假。
    // 当标签分类区发送变化时，会立即执行该函数，labelName是发送变化（选中/取消）的标签，newValue表示选中/取消的状态
    // 1.a)当选中一个标签时，要在屏幕显示上取消之前选中的标签（已完成），同时将当前标签写入到约束last_constraint的category内
    // 1.b)当取消一个标签时，一定取消的是上一次选中的标签，此时屏幕显示不需要做任何操作，同时将last_constraint内category置为null
    // 标签变化时，更新last_constraint并执行executeSearch
    labelChange(labelName, newValue){
      if (newValue) 
      {
        // 下面这一坨用来实现：点击新标签会去掉旧标签显示 
        Object.keys(this.category).forEach(key => {  
          if (key !== labelName) {  
            this.category[key] = false;  
          }  
        });
        this.last_constraint.category = labelName;
        this.executeSearch(); 
        // for debug
        // this.$message(`按${labelName}分类`);
      }
      else
      {
        this.last_constraint.category = null;
        this.executeSearch();
        // for debug
        // this.$message(`取消按${labelName}分类`);
      }
    },

    // 搜索框搜索功能 当用户按下搜索时执行 this.keyword为查询关键词，即输入框内的信息
    // 将关键词写入last_constraint的searchkey字段并执行一次executeSearch
    // 当关键词为空字符串时，将last_constrait中的searchkey置为null
    searchList()
    {
      this.last_constraint.searchkey = this.keyWord;
      this.executeSearch();
      // for debug
      this.$message(`搜索关键词：${this.keyWord}`);
    },

    // 排序功能 当用户点击排序区的任一字段时执行
    // 此时需要按key对应的属性(传入key的是order.TARGET)进行排序
    // 排序方式为升序(order_method=true)或降序(order_method=false)
    orderList(key, order_method)
    {
      this.last_constraint.order = key;
      this.last_constraint.if_forward = order_method;
      this.executeSearch();
      // for debug
      // this.$message(`排序字段：${key}, 排序方式${order_method? '升序':'降序'}`);
    },

    // 跳转商品详情
    routeGood(item)
    {
      this.$router.push({name: 'item', params:{id: item.id}});
    }

  },
  mounted() {

  },
  created() {
    //初始化页面时执行一次无约束搜索，并返回商品列表和总数给对应变量（这些都在executeSearch中完成）
    this.executeSearch();

    //用于显示页面结构的调试数据，完成函数后删除即可
    // this.totalGoods = 27
    // this.Goodlist=[
    //   {'id': 0, 'title': '辉瑞速诺阿莫西林克拉维酸钾片炎症感染 ','sold_num': 1798, 'price': 49.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 1, 'title': '可吉拉非泼罗尼滴剂猫用体外驱虫3支每盒 ','sold_num': 1699, 'price': 98.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 2, 'title': '普安特爱滴克非泼罗尼滴剂犬用体外驱虫','sold_num': 1640, 'price': 58.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 3, 'title': '普安特普拿杜犬猫通用体内广谱驱虫药','sold_num': 1625, 'price': 38.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 4, 'title': '普安特欣尔宁犬猫耳道耳炎耳垢护理药膏','sold_num': 1559, 'price': 29.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 5, 'title': '阿莫尔狗狗玩具磨牙耐咬绳结玩具宠物用品 ','sold_num': 994, 'price': 14.99, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 6, 'title': '艾宠仁家2代猫咪零食猫补水均衡营养厂家直销','sold_num': 867, 'price': 50.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 7, 'title': '宠物零食冻干桶 冻干猫零食500g鸡肉粒零食','sold_num': 850, 'price': 39.99, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 8, 'title': '大猫日记电动旋转猫玩具自动逗猫棒','sold_num': 823, 'price': 19.99, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 9, 'title': '疯狂的主人猫玩具逗猫棒自嗨解闷神器','sold_num': 654, 'price': 10.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 10, 'title': '辉瑞速诺阿莫西林克拉维酸钾片炎症感染 ','sold_num': 1798, 'price': 49.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 10, 'title': '可吉拉非泼罗尼滴剂猫用体外驱虫3支每盒 ','sold_num': 1699, 'price': 98.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 12, 'title': '普安特爱滴克非泼罗尼滴剂犬用体外驱虫','sold_num': 1640, 'price': 58.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 13, 'title': '普安特普拿杜犬猫通用体内广谱驱虫药','sold_num': 1625, 'price': 38.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 14, 'title': '普安特欣尔宁犬猫耳道耳炎耳垢护理药膏','sold_num': 1559, 'price': 29.00, 'image_url': require('../assets/temp/1.jpg')},
    //   {'id': 15, 'title': '辉瑞速诺阿莫西林克拉维酸钾片炎症感染 ','sold_num': 1798, 'price': 49.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 16, 'title': '可吉拉非泼罗尼滴剂猫用体外驱虫3支每盒 ','sold_num': 1699, 'price': 98.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 17, 'title': '普安特爱滴克非泼罗尼滴剂犬用体外驱虫','sold_num': 1640, 'price': 58.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 18, 'title': '普安特普拿杜犬猫通用体内广谱驱虫药','sold_num': 1625, 'price': 38.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 19, 'title': '普安特欣尔宁犬猫耳道耳炎耳垢护理药膏','sold_num': 1559, 'price': 29.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 20, 'title': '阿莫尔狗狗玩具磨牙耐咬绳结玩具宠物用品 ','sold_num': 994, 'price': 14.99, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 21, 'title': '艾宠仁家2代猫咪零食猫补水均衡营养厂家直销','sold_num': 867, 'price': 50.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 22, 'title': '宠物零食冻干桶 冻干猫零食500g鸡肉粒零食','sold_num': 850, 'price': 39.99, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 23, 'title': '大猫日记电动旋转猫玩具自动逗猫棒','sold_num': 823, 'price': 19.99, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 24, 'title': '疯狂的主人猫玩具逗猫棒自嗨解闷神器','sold_num': 654, 'price': 10.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 25, 'title': '辉瑞速诺阿莫西林克拉维酸钾片炎症感染 ','sold_num': 1798, 'price': 49.00, 'image_url': require('../assets/temp/2.jpg')},
    //   {'id': 26, 'title': '可吉拉非泼罗尼滴剂猫用体外驱虫3支每盒 ','sold_num': 1699, 'price': 98.00, 'image_url': require('../assets/temp/2.jpg')},
    // ]
  },
}
</script>

<style scoped>
body {  
  background-color: #FFFEF5; /* 你想要的颜色 */  
}

.eshopWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.shop-windows{
  display: flex;
  position: relative;
  flex-direction: column;
  justify-content: space-around; 
  margin-bottom: 30px;
  padding: 0px;
  height: 1100px;
  min-width: 1230px;
  width: 1230px;
  background-image: url("../assets/images/home/eshop/eshop_list.png");
}

.top-right-button {  
    position: absolute;
    top: 10px;  
    right: 10px; 
}

#shoplist {
  width: 1200px;
  height: 1209px;
  margin-left: 0px;
  margin-right: auto;
  margin-top: 30px;
  overflow: hidden;
}

.product-details {  
  display: flex;  
  align-items: center;
  flex-wrap: wrap; /* 允许换行 */
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
  margin: 0 10px 30px;
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

.titlecontent{
  display: flex;    
  align-items: center;
  margin-top: 10px;
  margin-bottom: 20px;
}

.shopButton{
  background-color: #e55e5e;
  border-color: #e55e5e;
}

.pagination{
  display: flex;  
  justify-content: center;  
  align-items: center;    
  height: 50px;
  margin-top: -20px;
  margin-bottom: 20px;
}

.show {  
  display: flex;  
  justify-content: space-between;
  align-items: flex-start;
  margin-top: 0px;
}

.label-selector-container {  
  min-width: 100px;
  margin-top: 60px;
}

.labelSelector{
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;
}

.secondLabel {  
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;
  margin-left: 20px;
} 

.orderSelector{
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;
}

.orderH{
  margin-bottom: 10px;
}

.orderItem p {
  font-size: 14px;
  margin-top: 0px;
  margin-left: 5px;
  margin-bottom: 10px;
  cursor: pointer;
  user-select: none; 
  -moz-user-select: none; 
  -ms-user-select: none;
  -webkit-user-select: none; 
}

</style>
