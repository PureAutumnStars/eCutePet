<!-- 
我的帖子
待完善功能：
    2. deletePost()
-->

<template>
    <div class="myPostWindow">
      <div class="myPost-bg">
        <div class="myPost-details">
          <ul v-for="(item,index) in paginatedPosts" :key="index" style="list-style-type: none; margin-left: -40px; margin-bottom: 0px; margin-top: 0px;">
              <li class="post">
                <i class="el-icon-delete-solid" style="margin-left: 10px; margin-right: 10px; margin-top: 22px;" @click="routeConfirm(item.id)"></i>
                <p class="tag-name">[{{genTagname(item.tag.id)}}]</p>  
                <h4 class="postTitle" @click="routePost(item.id)">{{item.title.length<=24?item.title:item.title.slice(0,24)+'...'}}</h4>
                <div class="postDetails">
                  <div class="author_time">
                    <p class="p_time">{{item.create_time.slice(0, 10)}}</p>
                  </div>
                  <div class="click_comment">
                    <p class="p_comment">{{item.click_num}}</p>
                  </div>
                  <div class="click_comment">
                    <p class="p_comment">{{item.favor_num}}</p>
                  </div>
                  <div class="click_comment_last">
                    <p class="p_comment">{{item.comment_num}}</p>
                  </div>
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
              :page-sizes="[9]"  
              :page-size="pageSize"  
              layout="total, sizes, prev, pager, next, jumper"  
              :total="totalPosts">  
            </el-pagination>  
      </div>
      <el-dialog
        title="警告"
        :visible.sync="dialogVisible"
        width="30%">
        <span>你确定要删除本条发帖吗？</span>
        <span>此操作不可撤回</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="deletePost(target_post)">确 定</el-button>
        </span>
      </el-dialog>
    </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { getPostsList, getSingleUser, deprecatePost } from "../api/api";
export default {
  name:'mypost',
  data() {
    return {
      currentPage: 1, 
      pageSize: 9, 
      totalPosts: 0,   
      dialogVisible: false,
      postList: [],
      target_post: -1,
      user_id: null,
      user_name: ''
    };
  },
  computed: {  
    // 计算帖子切片分页，可忽略
    paginatedPosts() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.postList.slice(start, end);  
    },  
  },
  methods: {
    // 获取用户名
    obtainUserName() {
      getSingleUser(this.user_id).then
      (response => 
        {
          if(response.status === 200) {
            this.user_name = response.data.username;
            //this.$message(`${this.user_name}`);
            this.obtainMyPosts();
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询用户详情时发生网络错误，请检查网络状况！');
        }
      )
    },
    // 获取我的帖子列表
    obtainMyPosts() {
      getPostsList(null, this.user_name, null, null, null, 'create_time,click_num,favor_num,comment_num', 1, 199).then
      (response =>
        {
          if(response.status === 200) {
            this.totalPosts = response.data.count;
            this.postList = response.data.results;
            // for debug
            console.log(`成功获取到您的帖子列表！`);
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              this.$message.error('很抱歉，您暂未登录，无法查看自己的帖子列表！');
              return;
            }
          }
          console.error('Enquiry Failed.', error);
          this.$message.error('查询帖子列表时发生网络错误，请检查网络状况！');
        }
      )
    },

    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },
    // 根据tag id 获取打印信息的函数， 可忽略
    genTagname(tag){
      if(tag === 1)
        return '宠物健康'
      if(tag === 2)
        return '萌宠日常'
      if(tag === 3)
        return '养宠经验'
    },
    routePost(index){
      this.$router.push({name: 'post', params:{id: index}});
    },
    routeConfirm(index){
      this.target_post = index;
      this.dialogVisible = true;
    },

    // TODO: 删除帖子 index为帖子id
    deletePost(index){
      this.dialogVisible = false;
      // 此处根据id调api删除帖子
      deprecatePost(index).then
      (response =>
        {
          if(response.status === 204) {
            // for debug
            console.log(`成功删除帖子，原帖子id为${index}`);
          }
        }
      ).catch
      (error =>
        {
          console.error('Delete Failed.', error);
          this.$message.error('删除帖子时发生网络错误，请检查网络状况！');
        }
      )
      //
      // 然后再get一次我的帖子列表 更新postlList
      this.obtainUserName();
      //
    },
  },
  mounted() {

  },
  created() {
    // 获取用户Id
    this.user_id = Cookies.get(`user_id`);

    // 初始化
    this.obtainUserName();
    
    // this.totalPosts = 13;
    // this.postList = [
    //   {
    //     "id": "0",
    //     "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？怎么花更少的钱改善猫咪掉毛问题？怎么花更少的钱改善猫咪掉毛问题？",
    //     "tag": {"id": 1},
    //     "brief_content": "猫咪掉毛严重怎么办",
    //     "author": {
    //       "id": 15,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "click_num": 98,
    //     "comment_num": 16,
    //     "favor_num": 20,
    //     "create_time": "2024-06-23T02:13:18.414Z",
    //     "modify_time": "2024-06-23T02:13:18.414Z"
    //   },
    //   {
    //     "id": "1",
    //     "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？怎么花更少的钱改善猫咪掉毛问题？怎么花更少的钱改善猫咪掉毛问题？",
    //     "tag": {"id": 1},
    //     "brief_content": "猫咪掉毛严重怎么办",
    //     "author": {
    //       "id": 15,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "click_num": 98,
    //     "comment_num": 16,
    //     "favor_num": 20,
    //     "create_time": "2024-06-23T02:13:18.414Z",
    //     "modify_time": "2024-06-23T02:13:18.414Z"
    //   },
    // ];
  }
}
</script>

<style scoped>
body {  
  background-color: #FFFEF5; /* 你想要的颜色 */  
}

.myPostWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.myPost-bg{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 10px;
  padding: 0px;
  height: 624px;
  min-width: 958px;
  width: 958px;
  background-image: url("../assets/images/home/community/mypost_list.png");
}

.myPost-details{
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  margin-top: 55px;
  width: 938px;
  height: 555px;
}

.pagination{
  margin-bottom: 20px;
}

.post{
  display: flex;
  flex-direction: row;
  border-bottom: 1px solid #cfcfcf;  
  height: 55px;
  margin-left: 0px;
  margin-top: 1px;
  margin-bottom: 0px;
  width: 936px;
}

.tag-name{
  margin-top: 19px;
  margin-right: 10px;
  font-size: 14px;
  margin-bottom: 0px;
}

.postTitle{
  margin-top: 18px;
  margin-bottom: 0px;
  text-align: left;  
  width: 400px;
}

.postTitle:hover{
  color:#EE6F60;
  cursor: pointer;
}

.postDetails{
  display: flex;
  flex-direction: row;
}

.author_time{
  width: 90px;
  margin-right: 30px;
  margin-left: 75px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.p_time{
  margin-top: 0px;
  margin-bottom: 0px;
  font-size: 14px;
  color: #080808;
}

.click_comment{
  width: 50px;
  display: flex;
  margin-right: 30px;
  flex-direction: column;
  justify-content: center;
}

.click_comment_last{
  width: 50px;
  display: flex;
  margin-right: 0px;
  flex-direction: column;
  justify-content: center;
}

.p_comment{
  margin-top: 0px;
  margin-bottom: 0px;
  font-size: 14px;
  color: #000000;
}
</style>
