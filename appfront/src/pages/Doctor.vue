<!-- 
医生 /Doctor
待完善功能：
1. created()
2. openAppoint()
3. confirmAppoint()
-->

<template>
  <div class="communityWindow">
    <img v-bind:src=doctor_title alt="">
    <div class="show">
      <div class="doctor-windows">
        <div class="doctor_details">
          <ul v-for="(item,index) in paginatedDoctor" :key="index" style="list-style-type: none; margin-left: 0px; margin-bottom: 0px; margin-top: 0px;">
              <li class="post">
                <div class="doctor_item">
                  <div class="doctor_img">
                    <img v-bind:src="item.real_image_url" alt="">
                  </div>
                  <div class="doctor_desc">
                    <div style="display: flex; flex-direction: row;">
                      <h3>{{item.real_name}}</h3>
                      <p style="margin-top: 6px; margin-left: 7px; 
                          margin-bottom: 0px; font-size: 14px; color: #886561;">执业兽医师</p>
                    </div>
                    <p class="doctor_desc_text">个人简介：{{item.description}}</p>
                    <div class="doctor_grade">
                      <div style="margin-top: 0px; margin-bottom: 0px; width: 200px; 
                      display: flex; flex-direction: row;">
                        <p style="color: #000000; margin-right: 10px;">文章: {{item.post_num}}</p>
                        <p style="color: #b3b3b3; margin-right: 10px;">|</p>
                        <p style="color: #000000;">接诊: {{item.reception_num}}</p>
                      </div>
                        <el-button type="primary" @click="openAppoint(item)"
                        style="background-color: #e55e5e; height: 40px; width: 120px; margin-left: 750px;
                            border-color: #e55e5e;">立即预约
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
              :total="totalDoctors">  
            </el-pagination>  
      </div>
      <el-dialog title="填写预约信息" :visible.sync="dialogFormVisible" width="40%">
        <div style="display: flex; flex-direction: row;">
          <p style="margin-top: 9px; margin-right: 10px; font-size: 16px;">预约日期</p>
          <el-date-picker  
            @change="UpdateTimes"
            v-model="date"  
            type="date"  
            placeholder="选择日期"   
            :picker-options="pickerOptionsDate">  
          </el-date-picker>
        </div>
        <div style="display: flex; flex-direction: row;">
          <p style="margin-top: 9px; margin-right: 10px; font-size: 16px;">预约时间</p>
          <el-select v-model="time" placeholder="选择时间" style="width: 220px;">  
            <el-option  
              v-for="time in availableTimes"  
              :key="time"  
              :label="time"  
              :value="time">  
            </el-option>  
          </el-select>  
        </div>
        <div style="display: flex; flex-direction: row;">
          <p style="margin-top: 9px; margin-right: 10px; font-size: 16px;">宠物名称</p>
          <el-input v-model="pet_name" type="primary" style="width: 85%;"></el-input>
        </div>
        <div style="display: flex; flex-direction: row;">
          <p style="margin-top: 9px; margin-right: 0px; font-size: 16px;">病情描述</p>
          <el-input
            type="textarea"
            :autosize="{ minRows: 6, maxRows: 6}"
            style="margin-left: 10px; width: 85%;"
            v-model="description">
          </el-input>
        </div>
        <div style="display: flex; flex-direction: row; justify-content: flex-end;">
          <el-button type="primary" :disabled="!isOK" @click="confirmAppoint(date, time, pet_name, description)"
            :style="{opacity: !isOK ? 0.5 : 1}"
            style="background-color: #e55e5e; height: 40px; width: 120px;
                   margin-top: 10px;border-color: #e55e5e;">确定
              <i class="el-icon-check"></i>
          </el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios, { all } from "axios";
export default {
  name:'community',
  data() {
    return {
      keyWord: '',
      doctor_title: require("../assets/images/home/doctor/doctor_title.png"),
      dialogFormVisible: false,
      pickerOptionsDate: {  
        disabledDate(time) {  
          const now = new Date();  
          const nextMonday = new Date(now.getFullYear(), now.getMonth(), now.getDate() + (8 - now.getDay()) % 7);  
          const nextSunday = new Date(nextMonday.getFullYear(), nextMonday.getMonth(), nextMonday.getDate() + 6); 
          return time.getTime() < nextMonday.getTime() || time.getTime() > nextSunday.getTime();  
        }  
      },  

      date: '',
      time: '',
      pet_name: '',
      description: '',
      appointList: '',
      
      originTimes: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00'],
      availableTimes: [],

      targetDoctor: 0,
      targetWeekday: 1,
      startDate: null,
      docList: [],
      currentPage: 1, 
      pageSize: 5, 
      totalDoctors: 0, 
      doctorTime: [],      

    };
  },
  methods: {
    formatDate(date) {  
      const year = date.getFullYear();  
      const month = String(date.getMonth() + 1).padStart(2, '0');  
      const day = String(date.getDate()).padStart(2, '0');  
      return `${year}-${month}-${day}`;  
    },
    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },
    hanzi2values(ph)
    {
        switch (ph) {
            case 'DayofWeekEnum.星期一':
                return "1";
                break;
            case 'DayofWeekEnum.星期二':
                return "2";
                break;
            case 'DayofWeekEnum.星期三':
                return "3";
                break;
            case 'DayofWeekEnum.星期四':
                return "4";
                break;
            case 'DayofWeekEnum.星期五':
                return "5";
                break;
            case 'DayofWeekEnum.星期六':
                return "6";
                break;
            default:
                return "7";
                break;
        }
    },
    initAvailableList(tdate)
    {
      let allAvailableTimes = []
      let weekday = tdate.slice(tdate.length-1, tdate.length)
      let onedata = null;
      let HanziWeekday = null;
      let n_weekday = null;
      let starttime = null;
      let endtime = null;
      let index_s = null;
      let index_e = null;
      let tempTimes = [];
      for(let i = 0; i < this.doctorTime.length; i++)
      {
        onedata = this.doctorTime[i];
        HanziWeekday = onedata.day_of_week
        n_weekday = this.hanzi2values(HanziWeekday);
        if(n_weekday === weekday){
          starttime = onedata.start_time.slice(0, 5);
          endtime = onedata.end_time.slice(0, 5);
          if(endtime === '23:59')
            endtime = '24:00'
          index_s = this.originTimes.findIndex(element => element === starttime);  
          index_e = this.originTimes.findIndex(element => element === endtime);
          tempTimes = this.originTimes.slice(index_s, index_e);
          allAvailableTimes = allAvailableTimes.concat(tempTimes)
        }
      }
      this.availableTimes = allAvailableTimes;
    },
    finalAvailableList(tdate)
    {
      let weekday = tdate.slice(tdate.length-1, tdate.length)
      let index = null;
      let onedata = null;
      let n_weekday = null;
      let sparedTime = null;
      for(let j = 0; j<this.appointList.length; j++)
      {
        onedata = this.appointList[j].appointment_time;
        n_weekday = onedata[9];
        if(weekday == n_weekday)
        {
          sparedTime = onedata.slice(11, 16)
          index = this.availableTimes.indexOf(sparedTime);  
          if (index !== -1) {  
            this.availableTimes.splice(index, 1);  
          }  
        }
      }
    },
    UpdateTimes(){
      this.initAvailableList(this.formatDate(this.date));
      this.finalAvailableList(this.formatDate(this.date));
    },


    // TODO：只需要在标记位置分别获取医生时间和预约记录即可
    openAppoint(item){
      // targetDoctor 医生id
      this.dialogFormVisible = true;
      this.targetDoctor = item.id;
      // TODO: 获取医生时间
      this.doctorTime = [
        {
            "id": "0",
            "day_of_week": 'DayofWeekEnum.星期一',
            "start_time": "09:00:00",
            "end_time": "11:00:00"
        },
        {
            "id": "1",
            "day_of_week": 'DayofWeekEnum.星期一',
            "start_time": "18:00:00",
            "end_time": "22:00:00"
        },
        {
            "id": "2",
            "day_of_week": 'DayofWeekEnum.星期四',
            "start_time": "08:00:00",
            "end_time": "12:00:00"
        },
        {
            "id": "3",
            "day_of_week": 'DayofWeekEnum.星期日',
            "start_time": "07:00:00",
            "end_time": "10:00:00"
        },
        {
            "id": "4",
            "day_of_week": 'DayofWeekEnum.星期日',
            "start_time": "13:00:00",
            "end_time": "23:59:59"
        },
      ]

      // TODO: 医生id 查询预约记录 起止时间直接摆烂设为空就行
      this.appointList = [
        {
          "id": "0",
          "doctor": null,
          "patient": null,
          "appointment_time": "2024-07-01T10:00:00.000Z",
          "pet_name": "string",
          "description": "",
          "status": "Pending",
          "comment": ""
        },
        {
          "id": "1",
          "doctor": null,
          "patient": null,
          "appointment_time": "2024-07-01T19:00:00.000Z",
          "pet_name": "string",
          "description": "",
          "status": "Pending",
          "comment": ""
        },
        {
          "id": "2",
          "doctor": null,
          "patient": null,
          "appointment_time": "2024-07-01T21:00:00.000Z",
          "pet_name": "string",
          "description": "",
          "status": "Pending",
          "comment": ""
        },
        {
          "id": "3",
          "doctor": null,
          "patient": null,
          "appointment_time": "2024-07-07T07:00:00.000Z",
          "pet_name": "string",
          "description": "",
          "status": "Pending",
          "comment": ""
        },
        {
          "id": "4",
          "doctor": null,
          "patient": null,
          "appointment_time": "2024-07-07T14:00:00.000Z",
          "pet_name": "string",
          "description": "",
          "status": "Pending",
          "comment": ""
        },
      ]

      this.initAvailableList(this.formatDate(this.date));
      this.finalAvailableList(this.formatDate(this.date));
    },

    //TODO: 新建预约 三个变量为所需数据 已处理好
    confirmAppoint(date, time, pet_name, description){
      let new_appointment_time = this.formatDate(date)+ 'T'+ time + ':00.000Z'
      let new_pet_name = pet_name;
      let new_desc = description;
      this.dialogFormVisible = false;
      this.$message("预约成功! 可在“我的预约”中查看和取消!")
    },
  },
  computed:{
    isOK(){
      if(this.date === '' || this.time === '' || this.description === '' || this.pet_name === '')
        return false
      else
        return true
    },
    paginatedDoctor() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.docList.slice(start, end);  
    },  
  },
  mounted() {

  },
  created() {
    const now = new Date();  
    const nextMonday = new Date(now.getFullYear(), now.getMonth(), now.getDate() + (8 - now.getDay()) % 7);  
    this.date = nextMonday

    // 获取医生列表 医生总数
    this.totalDoctors = 2;
    this.docList = [
      {
        "id": 0,
        "real_name": "缪慧君",
        "real_image_url": require("../assets/temp/d1.jpg"),
        "phone_number": "19975565866",
        "ID_number": "",
        "is_service": true,
        "description": "国家执业兽医师，从事小动物临床多年。任职过国内大型连锁宠物医院主治医生，专业技能扎实，为人亲和耐心，多次参加兽医再教育培训，尤其擅长内科疾病，猫科，肝肾，消化系统，神经内科，传染病，皮肤病，泌尿系统疾病。对于小动物常见呕吐、腹泻、咳嗽、尿闭尿血、传染病，消化道、呼吸道、泌尿道疾病有独特的治疗方法。擅长领域有犬猫皮肤病,神经内科疾病,以及犬细小猫鼻支等传染病,宠物呼吸道,消化道,泌尿道,生殖系统疾病的诊治，兔子,鼠科,貂,鸟类,乌龟咨询。",
        "reception_num": 19,
        "post_num": 5,
      },
      {
        "id": 1,
        "real_name": "E萌宠博士",
        "real_image_url": require("../assets/images/logo2.png"),
        "phone_number": "",
        "ID_number": "",
        "is_service": true,
        "description": "从事宠物疾病临床诊断、治疗以及宠物传染病、人畜共患病预防和控制的专业人员。面向动物医学行业，培养具有本专业必备的理论知识和专业技术应用能力，能胜任畜禽疾病免疫预防、疾病诊断与治疗、动物疫病检疫与兽医卫生检验、宠物疾病诊治与中兽医技术、兽医法规与行政执法、技术服务与推广等工作，并具有创新精神和较强实践能力的高级技术应用型人才。",
        "reception_num": 57,
        "post_num": 16,
      },
      

    ];

    
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
  width: 1100px;
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
