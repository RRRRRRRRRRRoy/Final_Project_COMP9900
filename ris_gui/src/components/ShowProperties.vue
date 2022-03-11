<template>
  <div class="TotalWrap">
    <el-row>
      <el-col :span="24">
        <el-card
          class="index-container"
          style="background-color: #788f77; border-radius: 10px; width: 100%"
        >
          <el-row justify="center">
            <el-col :span="21">
              <el-card class="Page_Title" style="border-radius: 10px">
                <el-row justify="center">
                  <h1><i class="el-icon-s-home" />Properties Overview</h1>
                </el-row>
              </el-card>
              <el-row>
                <el-col>
                  <el-card
                    v-for="(item, i) in list1"
                    :key="i"
                    class="TotalItem"
                    @change="CreateSelectSituation"
                    style="border-radius: 10px"
                  >
                    <el-row :span="6" justify="center">
                      <h3
                        style="cursor: pointer"
                        @click="checkingDetails(item.p_id)"
                      >
                        Properties {{ i + 1 }}
                      </h3>
                    </el-row>
                    <el-row class="el-property-info">
                      <el-card
                        class="content"
                        @click="checkingDetails(item.p_id)"
                        style="border-radius: 10px; cursor: pointer"
                      >
                        <el-row
                          >Renter Name:
                          {{ item.t_info.split("|||")[0] }}</el-row
                        >
                        <el-row
                          >E-mail: {{ item.t_info.split("|||")[1] }}</el-row
                        >
                        <el-row>Postcode: {{ item.postcode }}</el-row>
                        <el-row>Address: {{ item.address }}</el-row>
                        <!-- <div>p_id: {{ item.p_id }}</div> -->
                      </el-card>
                    </el-row>
                    <br />
                    <el-row justify="end">
                      <el-row v-if="selectedFlag">
                        <el-checkbox
                          v-model="SelectedObject[item.p_id]"
                          label="Selected"
                          border
                          size="large"
                        ></el-checkbox>
                      </el-row>
                      <el-row>
                        <el-button
                          type="danger"
                          icon="el-icon-delete"
                          @click="deleteProperties(item.p_id)"
                        ></el-button>
                      </el-row>
                    </el-row>
                  </el-card>
                  <el-card class="TotalItem" style="border-radius: 10px">
                    <el-row
                      type="flex"
                      justify="center"
                      align="middle"
                      style="height: 300px; cursor: pointer"
                      @click="GotoAddProperties()"
                      ><i class="el-icon-plus" />
                      <!-- <el-row
                        class="el-upload el-upload--picture-card"
                        tabindex="0"
                      >
                        <i class="el-icon-plus" />
                        <input
                          class="el-upload__input"
                          type="file"
                          name="file"
                          accept=""
                        />
                      </el-row> -->
                    </el-row>
                  </el-card>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>


<script>
import axios from "axios";
import { extractDateFormat } from "element-plus";
import { APIurl, Testurl } from "@/http";
import { ElMessage } from "element-plus";
import moment from "moment";
// import { useRouter } from 'vue-router'

export default {
  computed: {
    CreateSelectSituation() {
      for (let i = 0; i < this.list1.length; i++) {
        this.SelectedObject[this.list1[i].p_id] = false;
      }
      console.log(this.SelectedObject);
    },
  },
  data() {
    return {
      inspectionDate: "",
      selectedFlag: false,
      SelectedObject: {},
      list1: [],
      selectedInfo: {},
      selectedPid: "",
      counter: 0,
    };
  },
  mounted: function () {
    var mid = localStorage.getItem("id");
    axios
      .get(APIurl + `/property/Property_view/?m_id=${mid}`, {})
      .then((response) => {
        if (response.status === 200) {
          // alert("Success!")

          // localStorage.setItem("p_info", response.data.p_info);
          // window.pinfo = response.data.p_info
          for (let obj in response.data.p_info) {
            this.list1.push(response.data.p_info[obj]);
            // console.log(response.data.p_info[obj])
          }
        } else if (response.status === 404) {
          alert("This is a brand new account, plz adding properties!");
        }
      })
      .catch((error) => {
        // console.log(typeof error.response.status)
        if (error.response.status === 404) {
          ElMessage({
            showClose: true,
            message: "Please Add a Property Before Start",
            type: "error",
            center: true,
          });
        }
      });
  },
  methods: {
    changeSelectFlag() {
      this.selectedFlag = !this.selectedFlag;
    },
    deleteProperties(pid) {
      if (localStorage.getItem("plan") !== "null") {
        if (
          JSON.parse(localStorage.getItem("plan")).inPlan.places.includes(
            String(pid)
          )
        ) {
          ElMessage({
            type: "error",
            message: "The property is in your plan.",
            center: true,
          });
          return;
        }
      }
      // this.list1.splice(i, 1);
      axios
        .delete(APIurl + `/property/Property_manage/?id=${pid}`, {})
        .then((response) => {
          if (response.status === 200) {
            // alert("Current Property Delete successfully!")
            ElMessage({
              showClose: true,
              message: "Property Delete successfully",
              type: "success",
              center: true,
            });
            let addr = JSON.parse(localStorage.getItem("property_addr"));
            delete addr[String(pid)];
            localStorage.setItem("property_addr", JSON.stringify(addr));
            window.location.reload();
          }
        });
    },
    ClearInspections() {
      for (let i in this.SelectedObject) {
        this.SelectedObject[i] = false;
      }
      this.selectedFlag = !this.selectedFlag;
      this.selectedInfo = {};
    },
    SubmitInspections(formName) {
      for (let item in this.SelectedObject) {
        if (this.SelectedObject[item] === true) {
          // this.selectedInfo[item] =
          for (let item2 in this.list1) {
            if ("" + this.list1[item2].p_id === "" + item) {
              console.log(item);
              this.selectedInfo[item] = this.list1[item2].address.replace(
                /\s/g,
                "%20"
              );
            }
          }
        }
      }
      this.selectedPid = Object.keys(this.selectedInfo).join("|||");
      if (
        this.inspectionDate != "" &&
        JSON.stringify(this.selectedInfo) != "{}"
      ) {
        // axios.post(APIurl + "/route_plan/User/Route_Plan", {
        //   // current data binding in the report
        //   RoutePlan: this.selectedInfo,
        // });
        console.log(moment(this.inspectionDate).format("YYYY-MM-DD hh:mm:ss"));
        // this.inspectionDate = moment(this.inspectionDate).format("YYYY-MM-DD hh:mm:ss");
        console.log(this.selectedPid);
        axios.post(APIurl + "/email/m_inspection", {
          day: moment(this.inspectionDate).format("YYYY-MM-DD hh:mm:ss"),
          id: this.selectedPid,
        });
        ElMessage({
          showClose: true,
          message: "The Inspection Appointment has been sent",
          type: "success",
          center: true,
        });
      } else {
        ElMessage({
          showClose: true,
          message: "Please Check the Inspection Date and Selected Properties",
          type: "error",
          center: true,
        });
      }
    },
    GotoAddProperties() {
      this.$router.push({ name: "NewProperties" });
    },
    checkingDetails(pid) {
      // let index = this.list1.findIndex((x) => x.p_id == pid);
      // let detail_string = JSON.stringify(this.list1[index]);

      // localStorage.setItem("p_detail", detail_string);
      // console.log(localStorage.getItem("p_detail"))
      this.$router.push({ name: "propertyDetail", query: { id: pid } });
    },
    TestAutoComplete() {
      this.$router.push({ name: "MakeInspection", query: { id: 1 } });
    },
    testdata() {
      console.log(this.inspectionDate);
    },
  },
};
</script>

<style>
.TotalWrap {
  /* width: 80%; */
  margin: auto;
}
.TotalItem {
  float: left;
  width: 28%;
  border: #ddd solid 1px;
  margin: 0.8rem 2%;
  padding: 0.3rem;
  /* height: 17rem; */
}
.TotalItem div {
  padding: 0.15rem;
}
h3 {
  font-size: 1.3rem;
}
.el-property-info .content {
  font-size: 1rem;
}

.TotalItem .content {
  padding: 5px;
  width: 90%;
  margin: auto;
  border: #ddd solid 1px;
}

.el-upload {
  margin-top: 5rem;
}

.index-container {
  height: 75rem;
}
</style>


