<template>
  <div>
    <el-card
      class="index-container"
      style="background-color: #788f77; border-radius: 10px; width: 100%"
    >
      <el-row justify="center">
        <el-col :span="21">
          <el-card>
            <el-row justify="center">
              <h2>Modify Your Report</h2>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
      <br />
      <el-row justify="center">
        <el-col :span="20">
          <el-card>
            <template v-if="ModifyFlag">
              <h2>Report Title</h2>
              <el-input
                type="text"
                placeholder="Please input title"
                v-model="reportTitle"
                class="report-editarea"
              >
              </el-input>
              <el-row><br /></el-row>
            </template>
            <template v-else>
              <el-row justify="center">
                <h3>{{ reportTitle }}</h3>
              </el-row>
            </template>
            <template v-if="ModifyFlag">
              <el-input
                type="textarea"
                :rows="35"
                placeholder="Please Start Your Inspection report Content from Here"
                v-model="reportContent"
                class="report-editarea"
              >
              </el-input>
            </template>
            <template v-else>
              <p>{{ reportContent }}</p>
            </template>
            <el-row><br /></el-row>
            <template v-if="ModifyFlag">
              <el-row justify="center">
                <el-button type="success" round @click.prevent="UpdateReport()"
                  >Update</el-button
                >
                <el-button type="danger" round @click="CancelUpdate()"
                  >Cancel</el-button
                >
              </el-row>
            </template>
            <template v-else>
              <el-row justify="center">
                <el-button type="success" round @click.prevent="ModifyReport()"
                  >Modify</el-button
                >
                <el-button type="danger" round @click="BackToChooseReport()"
                  >Back</el-button
                >
              </el-row>
            </template>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import { extractDateFormat } from "element-plus";
import { ElMessage } from "element-plus";
import { Testurl, APIurl } from "@/http";
import moment from "moment";

export default {
  data() {
    return {
      ModifyFlag: false,
      reportContent: "",
      reportTitle: "",
      reportDate: "",
    };
  },
  mounted() {
    console.log(localStorage.getItem("Repo_info"));
    var report_info = JSON.parse(localStorage.getItem("Repo_info"));
    console.log(report_info);
    this.reportTitle = report_info.repo_title;
    this.reportDate = report_info.repo_date;
    this.reportContent = report_info.repo_content;
  },
  methods: {
    clearReport() {
      this.reportContent = "";
    },
    BackToChooseReport() {
      this.$router.push({ name: "ReportOverview", query: { id: "1" } });
    },
    ModifyReport() {
      this.ModifyFlag = !this.ModifyFlag;
    },
    UpdateReport() {
      // console.log(JSON.parse(localStorage.getItem("Repo_info")).repo_id);
      let current_repo = JSON.parse(localStorage.getItem("Repo_info"));
      let current_date = new Date();
      console.log();
      // console.log(current_date);
      if (this.reportContent != "" && this.reportTitle != "") {
        axios
          .patch(
            APIurl + `/Report/report_modify/?repo_id=${current_repo.repo_id}`,
            {
              p_id: current_repo.p_id,
              repo_content: this.reportContent,
              repo_title: this.reportTitle,
              repo_date: moment(current_date).format("YYYY-MM-DD HH:mm:ss"),
              last_visit_time: current_repo.last_visit_time,
            }
          )
          .catch((error) => {
            console.log(typeof error.response.status);
            if (error.response.status === 404) {
              ElMessage({
                showClose: true,
                message: "Fail To Update the New Report",
                type: "error",
                center: true,
              });
            }
          });
        ElMessage({
          showClose: true,
          message: "Report has been updated successfully!",
          type: "success",
          center: true,
        });
        this.ModifyFlag = !this.ModifyFlag;
      } else {
        ElMessage({
          showClose: true,
          message: "Please Check whether the title or the content is Empty!",
          type: "error",
          center: true,
        });
      }
    },
    CancelUpdate() {
      this.reportTitle = JSON.parse(
        localStorage.getItem("Repo_info")
      ).repo_title;
      this.reportDate = JSON.parse(localStorage.getItem("Repo_info")).repo_date;
      this.reportContent = JSON.parse(
        localStorage.getItem("Repo_info")
      ).repo_content;
      this.ModifyFlag = false;
    },
  },
};
</script>

<style scoped>
.index-container {
  height: 75rem;
}
</style>