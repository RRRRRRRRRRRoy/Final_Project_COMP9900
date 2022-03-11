<template>
  <div>
    <el-card
      class="index-container"
      style="background-color: #788f77; border-radius: 10px; width: 100%"
    >
      <el-row justify="center">
        <el-col :span="21">
          <el-card style="border-radius: 10px">
            <el-row justify="center">
              <h2>Adding a New Report</h2>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
      <br />
      <el-row justify="center">
        <el-col :span="20">
          <el-card style="border-radius: 10px">
            <el-input
              type="text"
              placeholder="Please input title"
              v-model="reportTitle"
              class="report-editarea"
            >
            </el-input>
            <el-row><br /></el-row>
            <el-input
              type="textarea"
              :rows="35"
              placeholder="Please Start Your Inspection report from Here"
              v-model="reportContent"
              class="report-editarea"
            >
            </el-input>
            <el-row><br /></el-row>
            <el-row justify="center">
              <el-button type="primary" round @click.prevent="submitReport()"
                >Submit</el-button
              >
              <el-button type="danger" round @click="clearReport()"
                >Clear</el-button
              >
              <el-button type="danger" round @click="BackToChoosePlan()"
                >Back</el-button
              >
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import { extractDateFormat } from "element-plus";
import { Testurl, APIurl } from "@/http";
import { ElMessage } from "element-plus";
import moment from "moment";

export default {
  data() {
    return {
      reportContent: "",
      reportTitle: "",
      reportDate: "",
    };
  },
  methods: {
    submitReport() {
      // console.log(this.reportContent);
      // this.$router.push("/success");
      let today = new Date();
      moment(today).format("YYYY-MM-DD hh:mm:ss");
      console.log();
      if (this.reportTitle != "" && this.reportContent != "") {
        axios
          .post("http://localhost:5000/Report/repo_manage/", {
            // current data binding in the report
            // not sure
            p_id: JSON.parse(localStorage.getItem("p_plan")).p_id,
            repo_content: this.reportContent,
            repo_title: this.reportTitle,
            repo_date: "" + moment(today).format("YYYY-MM-DD HH:mm:ss"),
            last_visit_time:
              "" + JSON.parse(localStorage.getItem("p_plan")).last_visit_time,
          })
          .then((response) => {
            if (response.status === 200) {
              ElMessage({
                showClose: true,
                message: "The report has been added successfully!",
                type: "success",
                center: true,
              });
              this.$router.push({ name: "ReportOverview", query: { id: "1" } });
            }
          })
          .catch((error) => {
            if (error.response.status === 404) {
              ElMessage({
                showClose: true,
                message:
                  "There is no Finished Plan, Please do the inspection first!",
                type: "error",
                center: true,
              });
            }
          });
      } else {
        // check null still question
        ElMessage({
          showClose: true,
          message: "The input content is empty",
          type: "error",
          center: true,
        });
      }
    },
    clearReport() {
      this.reportContent = "";
    },
    BackToChoosePlan() {
      this.$router.push({ name: "ReportAndPlan", query: { id: "1" } });
    },
  },
};
</script>

<style scoped>
.index-container {
  height: 75rem;
}
</style>