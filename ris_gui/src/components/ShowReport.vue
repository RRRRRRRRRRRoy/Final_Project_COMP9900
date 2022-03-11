<template>
  <el-card
    class="index-container"
    style="background-color: #788f77; border-radius: 10px; width: 100%"
  >
    <el-row type="flex" class="report-Header" justify="center">
      <el-col :span="21">
        <el-card class="box-card" style="border-radius: 10px">
          <el-row justify="center">
            <h1><i class="el-icon-collection" /> Reports Overview</h1>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <br />
    <el-row justify="center">
      <el-col :span="21">
        <el-card style="border-radius: 10px">
          <el-row>
            <el-col>
              <el-table :data="TestList" style="width: 100%" stripe>
                <el-table-column align="center" label="Last Modified Time">
                  <template #default="scope">
                    <i class="el-icon-time"></i>
                    <span style="margin-left: 10px">{{
                      scope.row.repo_date
                    }}</span>
                  </template>
                </el-table-column>
                <el-table-column align="center" label="Last Visit Date">
                  <template #default="scope">
                    <i class="el-icon-time"></i>
                    <span style="margin-left: 10px">{{
                      scope.row.last_visit_time
                    }}</span>
                  </template>
                </el-table-column>
                <el-table-column align="center" label="Property Address">
                  <template #default="scope">
                    <i class="el-icon-location-outline"></i>
                    <span style="margin-left: 10px">{{
                      scope.row.address.replace(', Australia', '')
                    }}</span>
                  </template>
                </el-table-column>

                <el-table-column align="center" label="Operation">
                  <template #default="scope">
                    <el-button
                      size="mini"
                      type="success"
                      @click="handleEdit(scope.$index, scope.row)"
                      >Show</el-button
                    >
                    <el-button
                      size="mini"
                      type="danger"
                      @click="handleDelete(scope.$index, scope.row)"
                      >Delete</el-button
                    >
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <br />
    <el-row type="flex" :span="18" class="report-content" justify="center">
      <el-button @click="AddNewReport()"> Add a New Report </el-button>
    </el-row>
  </el-card>
</template>



<script>
import axios from "axios";
import { extractDateFormat } from "element-plus";
import { APIurl, Testurl } from "@/http";
import { ElMessage } from "element-plus";
import moment from "moment";

export default {
  data() {
    return {
      TestList: [],
    };
  },
  mounted: function () {
    var mid = localStorage.getItem("id");
    // console.log(mid);
    axios
      .get(APIurl + `/Report/repo_overview/?m_id=${mid}`, {})
      .then((response) => {
        if (response.status === 200) {
          // alert("Success!")
          console.log(response.data);
          // localStorage.setItem("p_info", response.data.p_info);
          // window.pinfo = response.data.p_info
          for (let obj in response.data.repo_info) {
            this.TestList.push(response.data.repo_info[obj]);
            // console.log(response.data.p_info[obj])
          }
          console.log(this.TestList);
        }
      })
      .catch((error) => {
        console.log(typeof error.response.status);
        if (error.response.status === 404) {
          ElMessage({
            showClose: true,
            message: "Please Add a New Report to Continue!",
            type: "error",
            center: true,
          });
        }
      });
  },
  methods: {
    handleEdit(index, row) {
      localStorage.setItem("Repo_info", JSON.stringify(row));
      console.log(localStorage.getItem("Repo_info"));
      this.$router.push({ name: "ReportModify", query: { id: "1" } });
    },
    handleDelete(index, row) {
      var repo_id = row.repo_id;
      console.log(repo_id);
      axios
        .delete(APIurl + `/Report/repo_manage/?repo_id=${repo_id}`, {})
        .then((response) => {
          if (response.status === 200) {
            // alert("Current Property Delete successfully!")
            console.log(response);
            ElMessage({
              showClose: true,
              message: "Report Delete successfully",
              type: "success",
              center: true,
            });
            window.location.reload();
          }
        });
      // window.location.reload();
    },
    AddNewReport() {
      console.log(localStorage.getItem("id"));
      this.$router.push({ name: "ReportAndPlan", query: { id: "1" } });
    },
  },
};
</script>




<style scoped>
.el-upload__input {
  width: 1rem;
  height: 1rem;
}

.index-container {
  height: 75rem;
}
</style>