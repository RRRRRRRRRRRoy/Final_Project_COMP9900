<template>
  <el-card
    class="index-container"
    style="background-color: #788f77; border-radius: 10px; width: 100%"
  >
    <el-row type="flex" class="report-Header" justify="center">
      <el-col :span="21">
        <el-card class="box-card" style="border-radius: 10px">
          <el-row justify="center">
            <h1><i class="el-icon-collection" />Choose an Itinerary Plan</h1>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <br />
    <el-row justify="center">
      <el-col :span="18">
        <el-card style="border-radius: 10px">
          <el-row>
            <el-col>
              <el-table :data="TestList" style="width: 100%">
                <el-table-column align="center" label="Last Visit Date">
                  <template #default="scope">
                    <i class="el-icon-time"></i>
                    <span style="margin-left: 10px">
                      {{ scope.row.last_visit }}
                    </span>
                  </template>
                </el-table-column>

                <el-table-column align="center" label="Property Address">
                  <template #default="scope">
                    <i class="el-icon-location-outline"></i>
                    <span style="margin-left: 10px">{{
                      scope.row.address.replace(", Australia", "")
                    }}</span>
                  </template>
                </el-table-column>

                <el-table-column align="center" label="Operation">
                  <template #default="scope">
                    <el-button
                      size="mini"
                      type="primary"
                      @click="AddNewReport(scope.$index, scope.row)"
                      >Add a Report</el-button
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
      <el-button @click="backToOverview()"> Back to Overview </el-button>
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
      tableData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
        {
          date: "2016-05-04",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1517 弄",
        },
        {
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1519 弄",
        },
        {
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1516 弄",
        },
      ],
    };
  },
  mounted: function () {
    var mid = localStorage.getItem("id");
    // console.log(mid);
    axios
      .get(APIurl + `/Report/unreported_property/?m_id=${mid}`, {})
      .then((response) => {
        if (response.status === 200) {
          // alert("Success!")
          // console.log(response.data);
          // localStorage.setItem("p_info", response.data.p_info);
          // window.pinfo = response.data.p_info
          for (let obj in response.data.p_info) {
            this.TestList.push(response.data.p_info[obj]);
            // console.log(response.data.p_info[obj])
          }
          // console.log(this.TestList);
        }
      })
      .catch((error) => {
        // console.log(typeof error.response.status);
        console.log(localStorage.getItem("id"));
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
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    AddNewReport(index, row) {
      localStorage.setItem("p_plan", JSON.stringify(row));
      this.$router.push({ name: "AddInspectionReport", query: { id: "1" } });
    },
    backToOverview() {
      this.$router.push({ name: "ReportOverview", query: { id: "1" } });
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