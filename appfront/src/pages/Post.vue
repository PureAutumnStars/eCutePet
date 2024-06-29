<!-- 
发帖 /post
待完善功能：
    1. created()
    2. doFavor()
    3. confirmComment()
-->

<template>
    <div class="postWindow">
      <div v-if="ifFront_img" class="post-newer2">
        <div class="newer_details">
          <p class="post_title">[{{genTagname(post.tag.name)}}] {{post.title}}</p>
          <div class="content_details">
            <div class="avatar_name_time">
              <img v-bind:src=avatar_default class="item_img" alt="">
              <div class="name_time">
                <p class="name_p">{{post.author.username}}</p>
                <p class="time_p">{{post.create_time.slice(0,10)+" "+post.create_time.slice(11,19)}}</p>
              </div>
            </div>
            <div class="content_data">
              <p class="content_text">{{post.content}}</p>
              <div style="height: 400px; width: auto; margin-top: 10px;">
                <img v-bind:src=post.front_image alt="">
              </div>
              <div style="display: flex; flex-direction: rows; width: 800px; margin-left: 40px; margin-top: 80px;">
                <button class="post-Button" style="cursor: default;">
                  <i class="el-icon-view" style="margin-right: 6px;"></i>浏览 {{post.click_num}}
                </button>
                <button class="post-Button" @click="doFavor">
                  <i v-if="!isFavor" class="el-icon-star-off"></i>
                  <i v-else class="el-icon-star-on"></i>
                  收藏 {{post.favor_num}}
                </button>
                <button class="post-Button" @click="scrollComment">
                  <i class="el-icon-chat-dot-round" style="margin-right: 6px;"></i>评论 {{post.comment_num}}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="ifFront_img" class="post-comment2">
        <div class="comment_details">
          <ul v-for="(citem,index) in paginatedComments" :key="index" 
            style="list-style-type: none; margin-left: -40px; margin-top: 0px;">
              <li class="comment_item">
                <div class="avatar_name_time_comment">
                  <img v-bind:src=avatar_default class="item_img" alt="">
                  <div class="name_time">
                    <p class="name_p">{{citem.user.username}}</p>
                    <p class="time_p">{{citem.create_time.slice(0,10)+" "+citem.create_time.slice(11,19)}}</p>
                  </div>
                </div>
                <div class="comment_data">
                  <p class="comment_text">{{citem.content}}</p>
                </div>
              </li>
          </ul>
        </div>
      </div>

      <div v-if="!ifFront_img" class="post-newer">
        <div class="newer_details">
          <p class="post_title">[{{genTagname(post.tag.name)}}] {{post.title}}</p>
          <div class="content_details">
            <div class="avatar_name_time">
              <img v-bind:src=avatar_default class="item_img" alt="">
              <div class="name_time">
                <p class="name_p">{{post.author.username}}</p>
                <p class="time_p">{{post.create_time.slice(0,10)+" "+post.create_time.slice(11,19)}}</p>
              </div>
            </div>
            <div class="content_data">
              <p class="content_text">{{post.content}}</p>
              <div style="display: flex; flex-direction: rows; width: 800px; margin-left: 40px; margin-top: 110px;">
                <button class="post-Button" style="cursor: default;">
                  <i class="el-icon-view" style="margin-right: 6px;"></i>浏览 {{post.click_num}}
                </button>
                <button class="post-Button" @click="doFavor">
                  <i v-if="!isFavor" class="el-icon-star-off"></i>
                  <i v-else class="el-icon-star-on"></i>
                  收藏 {{post.favor_num}}
                </button>
                <button class="post-Button" @click="scrollComment">
                  <i class="el-icon-chat-dot-round" style="margin-right: 6px;"></i>评论 {{post.comment_num}}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!ifFront_img" class="post-comment">
        <div class="comment_details">
          <ul v-for="(citem,index) in paginatedComments" :key="index" 
            style="list-style-type: none; margin-left: -40px; margin-top: 0px;">
              <li class="comment_item">
                <div class="avatar_name_time_comment">
                  <img v-bind:src=avatar_default class="item_img" alt="">
                  <div class="name_time">
                    <p class="name_p">{{citem.user.username}}</p>
                    <p class="time_p">{{citem.create_time.slice(0,10)+" "+citem.create_time.slice(11,19)}}</p>
                  </div>
                </div>
                <div class="comment_data">
                  <p class="comment_text">{{citem.content}}</p>
                </div>
              </li>
          </ul>
        </div>
      </div>

      <div class="pagination">  
          <el-pagination  
            @size-change="handleSizeChange"  
            @current-change="handleCurrentChange"  
            :current-page="currentPage"  
            :page-sizes="[5]"  
            :page-size="pageSize"  
            layout="total, sizes, prev, pager, next, jumper"  
            :total="totalComments">  
          </el-pagination>  
      </div>

      <div class="newComment">
        <el-input class="p-comment-input" autosize type="textarea" 
              v-model="new_comment" maxlength="100" show-word-limit></el-input>
        <el-button type="primary" :disabled="!isOK" @click="confirmComment(new_comment)"
        :style="{opacity: !isOK ? 0.5 : 1}"
        style="background-color: #e55e5e; height: 50px; width: 160px; 
              margin-left: 1043px; margin-top: 20px;
              border-color: #e55e5e;">发布
          <i class="el-icon-s-promotion"></i>
        </el-button>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { getSinglePost, favorPost, getFavorPostList, getPostCommentList, createNewPostComment } from "../api/api";
export default {
  name:'post',
  data() {
    return {
      post_id: '',
      post: null,
      comments: null,
      new_comment: '',

      totalComments: 0,
      ifFront_img: false,
      isFavor: false,

      login_flag: false,

      // 当前页面， 每页大小（固定，用于请求时做参数）以及数量
      currentPage: 1, 
      pageSize: 5, 
      totalComments: 0, 
      
      avatar_default: require('../assets/images/logo.png')
    };
  },
  computed: {  
    paginatedComments() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.comments.slice(start, end);  
    },  
    isOK(){
      if(this.new_comment.length <= 0)
        return false
      else
        return true
    }
  },
  methods: {
    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },
    genTagname(tag){
      if(tag === '1')
        return '宠物健康'
      if(tag === '2')
        return '萌宠日常'
      if(tag === '3')
        return '养宠经验'
    },
    scrollComment(){
      window.scrollTo(0,3000);
    },

    // 检查登录
    checkLogin() {
      const token = Cookies.get('token');
      if(token) {
        this.login_flag = true;
      }
    },

    // 获取帖子详情
    obtainPostDetails() {
      getSinglePost(this.post_id).then
      (response =>
        {
          if(response.status === 200) {
            // for debug
            this.$message.success('获取帖子详情成功！');
            this.post = response.data;
            // if(response.data.front_image !== null) {
            //   this.ifFront_img = true;
            // }
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询帖子详情时发生网络错误，请检查网络状况！');
        }
      )
    },

    // 收藏帖子
    doFavor(){
      var favored_post_list = [];
      let favor_flag = false;
      getFavorPostList('create_time,post__favor_num,post__create_time,post__modify_time', 1, 199).then
      (response => 
        {
          if(response.status === 200) {
            if(response.data.count !== 0) {
              for(var i = 0; i < response.data.count; i++) {
                favored_post_list.push(response.data.results[i].post.id); 
              }
            }
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              // this.$message.error('很抱歉，您暂未登录，无法查看自己的收藏列表！');
              return;
            }
          }
          console.error('Enquiry Failed.', error);
          this.$message.error('查询帖子收藏列表时发生网络错误，请检查网络状况！');
        }
      )
      
      for (var i = 0; i < favored_post_list.length; i++) {
        if(this.post_id === favored_post_list[i]) {
          favor_flag = true;
          break;
        }
      }
      if(favor_flag) {
        this.isFavor = true;
      }

      if(this.login_flag) {
        this.isFavor = !this.isFavor;
        if(this.isFavor) {
          favorPost(this.post_id);
          this.post.favor_num = this.post.favor_num + 1;
        }
        else {
          favorPost(this.post_id);
          this.post.favor_num = this.post.favor_num - 1;
        }
      }
      else {
        this.$message('未登录用户无法收藏帖子，正在跳转到登录界面~');
        this.$router.push('/login');
      }
    },

    // 收藏帖子初始化
    favorInit(is_login) {
      if(is_login) {
        getFavorPostList('create_time,post__favor_num,post__create_time,post__modify_time', 1, 199).then
        (response => 
          {
            var favored_post_list = [];
            let favor_flag = false;
            if(response.status === 200) {
              if(response.data.count !== 0) {
                for(var i = 0; i < response.data.count; i++) {
                  favored_post_list.push(response.data.results[i].post.id); 
                }
              }
              for (var i = 0; i < favored_post_list.length; i++) {
                if(this.post_id === favored_post_list[i]) {
                  favor_flag = true;
                  break;
                }
              }
            }
            if(favor_flag) {
              this.isFavor = true;
            }
          }
        )
      }
    },

    // 获取评论列表
    obtainComments() {
      getPostCommentList(this.post_id, '', '', 'create_time,modify_time', 1, 199).then
      (response =>
        {
          if(response.status === 200) {
            this.totalComments = response.data.count;
            this.comments = response.data.results;
            // for debug
            // this.$message(`成功获取到评论列表，总评论数为${this.totalComments}`);
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询该帖子的评论列表时发生网络错误，请检查网络状况！');
        }
      )
    },

    // 新建评论 text为评论内容
    confirmComment(text){
      createNewPostComment(this.post_id, text).then
      (response =>
        {
          if(response.status === 201) {
            // for debug
            this.$message.success('评论成功！');
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              this.$message.error('未登录用户无法评论！');
              return;
            }
          }
          console.error('Comment Failed.', error);
          this.$message.error('评论帖子时发生网络错误，请检查网络状况！');
        }
      )
    }
  },
  mounted() {

  },
  created() {
    const {id} = this.$route.params;
    this.post_id = id;

    // 检查登录情况，设置this.if_login
    this.checkLogin();

    // 初始化：获取帖子详情
    this.obtainPostDetails();

    // 初始化：是否已收藏
    this.favorInit(this.login_flag);
    // this.post = {
    //   "id": "114514",
    //   "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？",
    //   "tag": {
    //     "id": 1,
    //     "name": "string",
    //     "description": "",
    //     "create_time": "2024-06-21T00:02:00.377Z",
    //     "modify_time": "2024-06-21T00:02:00.377Z"
    //   },
    //   "front_image": require("../assets/temp/1.png"),
    //   "brief_content": "猫咪掉毛严重的解决方法",
    //   "author": {
    //     "id": 17,
    //     "username": "清秋自有梧桐在"
    //   },
    //   "content": "家里的猫毛满天飞，就连吃饭的碗里都是猫咪的毛发，每天都有扫不完的猫毛怎么办？相信很多铲屎官都被这个问题困扰了很多年，而且不知道如何去改善。其实减少猫咪掉毛的方法并不困难，只需做好几点日常工作即可，详情请往下看。一开始，我认为猫咪掉毛可能是品种、季节、正常新陈代谢等原因导致的，所以每天只能默默地忍受猫毛给生活带来的各种不便（包括但不仅限于喝水喝一半发现有猫毛、每天数次从鼻子里扯出几根猫毛、冬天穿大衣出门前必需先粘猫毛……）。",
    //   "click_num": 191,
    //   "comment_num": 9,
    //   "favor_num": 81,
    //   "create_time": "2024-06-26T07:02:00.377Z",
    //   "modify_time": "2024-06-26T07:02:00.377Z"
    // };

    // 初始化：获取评论列表
    this.obtainComments();
    // this.totalComments = 7;
    // this.comments = [
    //   {
    //     "id": "0",
    //     "user": {
    //       "id": 13,
    //       "username": "随便啦"
    //     },
    //     "post": "114514",
    //     "content": "确实确实, 说的太对了(捂脸)..",
    //     "create_time": "2024-06-26T08:48:08.261Z",
    //     "modify_time": "2024-06-26T08:48:08.261Z"
    //   },
    //   {
    //     "id": "1",
    //     "user": {
    //       "id": 13,
    //       "username": "随便啦"
    //     },
    //     "post": "114514",
    //     "content": "后文呢！楼主继续更新！",
    //     "create_time": "2024-06-26T10:23:08.261Z",
    //     "modify_time": "2024-06-26T10:23:08.261Z"
    //   },
    //   {
    //     "id": "2",
    //     "user": {
    //       "id": 17,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "post": "114514",
    //     "content": "别急别急, 在准备周六的软工验收，晚上马上写！",
    //     "create_time": "2024-06-26T14:03:14.261Z",
    //     "modify_time": "2024-06-26T14:03:14.261Z"
    //   },
    //   {
    //     "id": "3",
    //     "user": {
    //       "id": 13,
    //       "username": "随便啦"
    //     },
    //     "post": "114514",
    //     "content": "楼主也是大学生啊...软件专业吗..",
    //     "create_time": "2024-06-26T15:09:38.261Z",
    //     "modify_time": "2024-06-26T15:09:38.261Z"
    //   },
    //   {
    //     "id": "4",
    //     "user": {
    //       "id": 21,
    //       "username": "理塘田所浩二十"
    //     },
    //     "post": "114514",
    //     "content": "自己已经习惯猫毛了,但是女朋友猫毛过敏，所以一般不会来我妈家里。周末的时候我和她都在外面住。看来以后是没机会自己养猫了，考虑下养只鼠鼠。",
    //     "create_time": "2024-06-26T18:03:21.261Z",
    //     "modify_time": "2024-06-26T18:03:21.261Z"
    //   },
    //   {
    //     "id": "5",
    //     "user": {
    //       "id": 13,
    //       "username": "随便啦"
    //     },
    //     "post": "114514",
    //     "content": "蹲蹲蹲",
    //     "create_time": "2024-06-26T18:48:43.261Z",
    //     "modify_time": "2024-06-26T18:48:43.261Z"
    //   },
    //   {
    //     "id": "6",
    //     "user": {
    //       "id": 17,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "post": "114514",
    //     "content": "不是软件专业, 人工智能专业的, 纯纯nt玩意, 一整个忙死...",
    //     "create_time": "2024-06-27T01:24:08.261Z",
    //     "modify_time": "2024-06-26T01:24:08.261Z"
    //   },
    // ]
    
  }
}
</script>

<style scoped>
.postWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.post-newer{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 363px;
  width: 1230px;
  background-image: url("../assets/images/home/community/post_newer.png");
}

.post-newer2{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 760px;
  width: 1230px;
  background-image: url("../assets/images/home/community/post_newer2.png");
  margin-bottom: 0px;
}

.post-comment{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 1290px;
  width: 1230px;
  background-image: url("../assets/images/home/community/post_comment.png");
  margin-top: -53px;
}

.post-comment2{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 1290px;
  width: 1230px;
  background-image: url("../assets/images/home/community/post_comment.png");
  margin-top: -24px;
}

.newer_details{
  width: 1210px;
  height: 335px;
  margin-left: 10px;
  margin-top: 13px;
}

.post_title{
  color: #ffffff;
  font-size: 19px;
  margin-top: 10px;
  margin-bottom: 0px;
  text-align: left;
  margin-left: 20px;
}

.content_details{
  display: flex;
  flex-direction: row;
}

.avatar_name_time{
  margin-top: 15px;
  width: 295px;
  height: 286px;
  display: flex;
  flex: row;
}

.avatar_name_time img{
  width: 120px;
  height: 120px;
  margin-left: 20px;
  margin-top: 20px;
}

.name_time {
  margin-top: 30px;
  margin-left: 10px;
} 

.name_p{
  margin-bottom: 5px;
  font-size: 18px;
  font-weight: bold;
  text-align: left;
}

.time_p{
  margin-top: 0px;
  margin-bottom: 3px;
  font-size: 12px;
  color: #878879;
  text-align: left;
}

.content_data{
  width: 885px;
  height: 278px;
  margin-top: 20px;
  margin-left: 15px;
  display: flex;
  flex-direction: column;
}

.content_text{
  text-align: left;
  margin-top: 20px;
  margin-left: 10px;
}

.post-Button{
  margin-top: 0px;
  margin-left: 10px;
  width: 110px;
  height: 40px;
  background-color: #B4D65F;
  border-color: transparent;
  user-select: none; 
  -moz-user-select: none; 
  -ms-user-select: none;
  -webkit-user-select: none; 
  cursor: pointer;
  font-size: 16px;
  color: #ffffff;
}

.comment_details{
  width: 1210px;
  height: 1265px;
  margin-left: 10px;
  margin-top: 13px;
}
  
.comment_item{
  width: 1210px;
  height: 250px;
  margin-bottom: -15px;
  margin-top: 0px;
  display: flex;
  flex-direction: row;
}

.avatar_name_time_comment{
  width: 295px;
  height: 286px;
  display: flex;
  flex: row;
}

.avatar_name_time_comment img{
  width: 120px;
  height: 120px;
  margin-left: 20px;
  margin-top: 20px;
}

.comment_data{
  width: 920px;
  height: 250px;
  display: flex;
  flex-direction: column;
}

.comment_text{
  text-align: left;
  margin-top: 40px;
  margin-left: 30px;
  margin-right: 15px;
}

.pagination{
  display: flex;  
  justify-content: center;  
  align-items: center;    
  height: 50px;
  margin-top: -40px;
  margin-bottom: 0px;
}

.newComment{
  background-image: url("../assets/images/home/community/post_new_comment.png");
  width: 1230px;
  height: 295px;
  display: flex;
  flex-direction: column;
  margin-top: -20px;
}

.p-comment-input{
  margin-top: 80px;
  margin-left: 20px;
  width: 1180px;
  height: 100px;
  border: 1px solid #eeeeee;
  padding-bottom: 10px;
  font-size: 16px;
}

.newComment>>>.el-textarea__inner {
  border: 0;
  resize: none;
  background-color: transparent;
}


</style>
