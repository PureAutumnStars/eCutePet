<!-- 
我的预约 /Doctor
待完善功能：
1. created()
2. cancelAppoint()
-->

<template>
  <div class="communityWindow">
    <div class="show">
      <div class="doctor-windows">
        <div class="doctor_details">
          <ul v-for="(item,index) in paginatedAppoint" :key="index" style="list-style-type: none; margin-left: 0px; margin-bottom: 0px; margin-top: 0px;">
              <li class="post">
                <div class="doctor_item">
                  <div class="doctor_desc">
                    <div style="display: flex; flex-direction: row;">
                      <h3 style="color: #000000;">预约信息——单号：{{item.id}}</h3>
                    </div>
                    <div style="display: flex; flex-direction: row;">
                      <p style="color: #000000; margin-right: 10px;"><b>医生姓名</b>：{{item.doctor.real_name}}</p>
                      <p style="color: #000000; margin-right: 10px;"><b>宠主姓名</b>：{{item.patient.real_name}}</p>
                      <p style="color: #000000; margin-right: 10px;"><b>宠物名字</b>：{{item.pet_name}}</p>
                      <p style="color: #000000; margin-right: 10px;"><b>宠物主联系方式</b>：{{item.patient.phone_number}}</p>
                    </div>
                    <div style="display: flex; flex-direction: row;">
                      <p style="color: #000000; margin-right: 10px;"><b>病情描述</b>：{{item.description}}</p>
                      <p style="color: #000000; margin-right: 10px;"><b>预约时间</b>：{{item.appointment_time.slice(0,19)}}</p>
                    </div>
                    <div style="display: flex; flex-direction: row;">
                      <p style="color: #000000; margin-right: 0px;"><b>预约单状态</b>：</p>
                      <p style="color: #e55e5e; margin-right: 10px;">{{genStatus(item.status)}}</p>
                      <el-button v-if="!isDoctor" type="primary" :disabled="item.status!=='Pending'" @click="cancelAppoint(item)"
                        :style="{opacity: item.status!=='Pending' ? 0.5 : 1}"
                        style="background-color: #e55e5e; height: 40px; width: 120px;
                              margin-top: 0px;border-color: #e55e5e; margin-left: 900px;">
                              {{item.status!=='Pending' ? '不可操作':'取消预约'}}
                      </el-button>
                    </div>
                  </div>
                </div>
              </li>
          </ul>
        </div>
      </div>
      <div class="pagination" style="margin-top: -30px; margin-bottom: 20px;">  
            <el-pagination  
              @size-change="handleSizeChange"  
              @current-change="handleCurrentChange"  
              :current-page="currentPage"  
              :page-sizes="[5]"  
              :page-size="pageSize"  
              layout="total, sizes, prev, pager, next, jumper"  
              :total="totalAppoint">  
            </el-pagination>  
      </div>
    </div>
  </div>
</template>

<script>
import axios, { all } from "axios";
import Cookies from "js-cookie";
export default {
  name:'community',
  data() {
    return {
      currentPage: 1, 
      pageSize: 5, 
      totalAppoint: 0, 

      appointList: [],
    };
  },
  methods: {
    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },
    genStatus(s)
    {
      switch (s) {
        case 'Pending':
          return '待确认'
          break;
        case 'Confirmed':
          return '已确认'
          break;
        case 'Canceled':
          return '已取消'
          break;
        case 'Completed':
          return '已完成'
          break;
        default:
          return s
          break;
      }
    },

    //TODO 改变订单状态为取消
    cancelAppoint(item){
      //能执行此函数的预约单状态一定为pending item.id为预约单id
      //
      // 
    },
    
  },
  computed:{
    paginatedAppoint() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.appointList.slice(start, end);  
    },  
    isDoctor(){
      // 判断用户身份为患者/医生
        return true;
    },
  },
  mounted() {

  },
  created() {
    // TODO 获取我的预约列表
    this.totalAppoint = 3;
    this.appointList = [
      {
        "id": "0",
        "doctor": {
          "real_name": "缪慧君",
        },
        "patient": {
          "id": 0,
          "real_name": "苗梓萌",
          "phone_number": "19975565866"
        },
        "appointment_time": "2024-07-07T16:00:00.000Z",
        "pet_name": "豆豆",
        "description": "咳嗽与抓挠复查",
        "status": "Pending",
      },
      {
        "id": "1",
        "doctor": {
          "real_name": "缪慧君",
        },
        "patient": {
          "id": 0,
          "real_name": "苗梓萌",
          "phone_number": "19975565866"
        },
        "appointment_time": "2024-07-04T16:00:00.000Z",
        "pet_name": "豆豆",
        "description": "咳嗽与抓挠",
        "status": "Confirmed",
      },
      {
        "id": "2",
        "doctor": {
          "real_name": "缪慧君",
        },
        "patient": {
          "id": 0,
          "real_name": "苗梓萌",
          "phone_number": "19975565866"
        },
        "appointment_time": "2024-07-01T16:00:00.000Z",
        "pet_name": "豆豆",
        "description": "频繁咳嗽，症状较为剧烈，有些担心所以约下看看",
        "status": "Completed",
      },
    ]
  },
}
</script>

<style scoped>
body {  
  background-color: #FFFEF5;
}

.communityWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.doctor-windows{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 980px;
  min-width: 1230px;
  width: 1230px;
  background-image: url("../assets/images/home/doctor/doctor_list.png");
}

.doctor_details{
  display: flex;
  flex-direction: column;
  align-items: center; 
  margin-bottom: 30px;
  margin-top: 10px;
  margin-left: 10px;
  padding: 0px;
  height: 970px;
  min-width: 1210px;
  width: 1210px;
}

.doctor_item{
  display: flex;
  flex-direction: row;
  width: 1180px;
  height: 168px;
  padding: 10px;
  border-bottom: 1px solid #d4d4d4;
}

.post{
  margin-left: -40px;
}

.doctor_img{
  width: 90px;
  height: 90px;
  margin-right: 10px;
}

.doctor_img img{
  width: 90px;
  height: 90px;
  border-radius: 20%;
}

.doctor_desc{
  width: 1200px;
  height: 170px;
  margin-top: 0px;
}

.doctor_desc h3{
  text-align: left;
  margin-top: 0px;
  margin-bottom: 0px;
  color: #7C5252;
}

.doctor_desc_text{
  margin-top: 10px;
  text-align: left;
  height: 75px;
}

.doctor_grade{
  display: flex;
  flex-direction: row;
}

</style>
