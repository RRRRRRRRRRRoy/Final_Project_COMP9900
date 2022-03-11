<template>
  <div>
    <el-card
      class="index-container"
      style="background-color: #788f77; border-radius: 10px; width: 100%"
    >
      <div>
        <el-row type="flex" justify="center">
          <el-col :span="21">
            <el-card
              class="property-image-card uploading-img-card"
              justify="center"
              style="border-radius: 10px"
            >
              <h3>Property Picture</h3>
              <el-row type="flex" class="properties-info" justify="center">
                <el-col>
                  <el-upload
                    action="https://www.fastmock.site/mock/621c7b950c9ece8cc619775913e4d7ee/test"
                    list-type="picture-card"
                    :auto-upload="false"
                    :limit="5"
                    :on-exceed="handleExceed"
                    :on-preview="handlePictureCardPreview"
                    :on-remove="handleRemove"
                    :on-change="changePicture"
                  >
                    <i
                      class="el-icon-plus"
                      style="width:100%, height:450px"
                    ></i>
                  </el-upload>
                  <el-dialog :visible.sync="dialogVisible">
                    <img width="100%" :src="dialogImageUrl" alt="" />
                  </el-dialog>
                </el-col>
              </el-row>
            </el-card>
          </el-col>
        </el-row>
        <el-row><br /><br /></el-row>
        <el-row justify="center">
          <el-col :span="21">
            <el-card class="property-info-card" style="border-radius: 10px">
              <h3>Property information</h3>
              <el-row type="flex" class="properties-infor" justify="center">
                <el-col :span="24">
                  <el-form
                    class="properties-information"
                    :rules="rules"
                    :model="renterInfo"
                    ref="renterInfo"
                    label-width="150px"
                  >
                    <el-col>
                      <el-form-item label="Renter Name:" prop="renterName">
                        <el-input
                          v-model="renterInfo.renterName"
                          placeholder="Renter Name"
                          clearable
                          style="width: 100%"
                        />
                      </el-form-item>
                      <el-form-item label="Renter Email:" prop="renterEmail">
                        <el-input
                          v-model="renterInfo.renterEmail"
                          placeholder="Renter Email Address"
                          type="email"
                          clearable
                          style="width: 100%"
                        />
                      </el-form-item>
                      <el-form-item label="Address:" prop="propertiesAddress">
                        <vue-google-autocomplete
                          ref="propertyAddress"
                          id="map"
                          class="Teest address-input"
                          classname="form-control"
                          placeholder="Please enter your address"
                          v-model="renterInfo.propertiesAddress"
                          v-on:placechanged="getAddressPrediction"
                          country="au"
                          style="width: 100%"
                        >
                        </vue-google-autocomplete>
                      </el-form-item>
                    </el-col>
                    <el-col>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</el-col>
                    <el-col>
                      <el-form-item label="Property Postcode:" prop="postCode">
                        <el-input
                          v-model="renterInfo.postCode"
                          placeholder="Properties Postcode"
                          style="width: 100%"
                          clearable
                        />
                      </el-form-item>
                      <el-form-item
                        label="Rent Start Date:"
                        prop="rentStartDate"
                      >
                        <el-date-picker
                          style="width: 100%"
                          v-model="renterInfo.rentStartDate"
                          type="date"
                          placeholder="Select Start Date"
                        >
                        </el-date-picker>
                      </el-form-item>
                      <el-form-item label="Rent End Date:" prop="rentEndDate">
                        <el-date-picker
                          style="width: 100%"
                          @change="dateSequenceCheck"
                          v-model="renterInfo.rentEndDate"
                          type="date"
                          placeholder="Select End Date"
                        >
                        </el-date-picker>
                        <div class="el-form-item__error" v-if="errors.endDate">
                          Invalid Rental End Date.
                        </div>
                      </el-form-item>
                    </el-col>
                  </el-form>
                </el-col>
              </el-row>
              <el-row type="flex" justify="center">
                <el-button
                  type="success"
                  @click="submitPropertyInfo('renterInfo')"
                  style="font-family: 'Times New Roman', Times, serif"
                >
                  Submit
                </el-button>
                <div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>
                <el-button
                  type="danger"
                  @click="clearPropertyInfo()"
                  style="font-family: 'Times New Roman', Times, serif"
                >
                  Clear
                </el-button>
              </el-row>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <el-row><br /><br /></el-row>
      <div>
        <el-row type="flex" class="properties-location" justify="center">
          <el-col :span="21">
            <el-card
              class="box-card"
              justify="center"
              style="border-radius: 10px"
            >
              <h3>Property location</h3>
              <!-- <div class="properties-location"></div> -->
              <!-- AIzaSyDb8WLdQ91JzeQwG9BJVVJ2L9bCo0V8ZCc   -->
              <GoogleMap
                class="Google-map"
                api-key="AIzaSyDb8WLdQ91JzeQwG9BJVVJ2L9bCo0V8ZCc"
                :center="center"
                :zoom="15"
              >
                <Marker :options="{ position: center }" />
              </GoogleMap>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, reactive } from "vue";
import { GoogleMap, Marker } from "vue3-google-map";
import { Testurl, APIurl } from "@/http";
import emailFormatCheck from "../utils/formValidator/emailFormatCheck.js";
import postCodeCheck from "../utils/formValidator/postCodeCheck.js";
// import AddressAnalyzer from "../utils/AddressAnalyzer.js";
import axios from "axios";
import moment from "moment";
import { ElMessage } from "element-plus";
import VueGoogleAutocomplete from "vue-google-autocomplete";

export default defineComponent({
  components: { GoogleMap, Marker, VueGoogleAutocomplete },
  computed: {
    dateSequenceCheck() {
      // alert("1")
      let date1 = new Date(Date.parse(this.renterInfo.rentStartDate));
      let date2 = new Date(Date.parse(this.renterInfo.rentEndDate));
      if (date1 > date2) {
        // alert("2")
        this.errors.endDate = true;
      } else {
        this.errors.endDate = false;
      }
    },
  },
  data() {
    return {
      center: { lat: -33.87253523324751, lng: 151.20714941648205 },
      dialogImageUrl: "",
      dialogVisible: false,
      rulerChecker: true,
      errors: {
        endDate: "",
        emptyAddress: "",
      },
      renterInfo: reactive({
        renterName: "",
        renterEmail: "",
        propertiesAddress: "",
        postCode: "",
        lastVisit: "9999-12-31",
        rentStartDate: "",
        rentEndDate: "",
        longitude: 0,
        latitude: 0,
        pictures: {},
      }),
      // GoogleMapKey: 'AIzaSyDb8WLdQ91JzeQwG9BJVVJ2L9bCo0V8ZCc',
      rules: {
        renterName: [
          {
            required: true,
            message: "Please enter the renter name.",
            trigger: "blur",
          },
        ],
        renterEmail: [
          {
            required: true,
            message: "Please enter the email.",
            trigger: "blur",
          },
          {
            validator: emailFormatCheck,
            trigger: "blur",
          },
        ],
        propertiesAddress: [
          {
            required: true,
            message: "Please enter the renter address.",
            trigger: "blur",
          },
        ],
        postCode: [
          {
            required: true,
            message: "Please enter the postcode.",
            trigger: "blur",
          },
          {
            validator: postCodeCheck,
            trigger: "blur",
          },
        ],
        rentStartDate: [
          {
            required: true,
            message: "Please enter the renter start date.",
            trigger: "blur",
          },
        ],
        rentEndDate: [
          {
            required: true,
            message: "Please enter the renter end date.",
            trigger: "blur",
          },
        ],
      },
    };
  },
  mounted() {
    this.$refs.propertyAddress.focus();
  },
  methods: {
    handleExceed(file, filelist) {
      ElMessage({
        showClose: true,
        message: "At Most 5 Pictures.",
        type: "error",
        center: true,
      });
    },
    changePicture(file, filelist) {
      const isLt2M = file.size / 1024 / 1024 < 2;
      const isImg = ["image/jpg", "image/png", "image/jpeg"].includes(
        file.raw.type
      );
      if (isLt2M && isImg) {
        let pictureBuffer = { 0: "", 1: "", 2: "", 3: "", 4: "" };
        for (let i in filelist) {
          let reader = new FileReader();
          reader.readAsDataURL(filelist[i].raw);
          reader.onload = () => {
            pictureBuffer[i] = reader.result;
          };
        }
        this.renterInfo.pictures = pictureBuffer;
      } else {
        ElMessage({
          message:
            "Picture should be less than 2MB and in .jpg, .png or .jpeg format.",
          type: "error",
          center: true,
        });
        return;
      }
    },
    handleRemove(file, fileList) {
      console.log(fileList);
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    modifyDate(Date) {
      return moment(Date).format("YYYY-MM-DD");
    },
    getAddressPrediction(addressData, placeResultData, id) {
      this.renterInfo.propertiesAddress = placeResultData.formatted_address;
      // console.log(placeResultData.formatted_address)
      // console.log(addressData.latitude)
      // console.log(addressData.longitude)
      // console.log(addressData.postal_code)
      this.renterInfo.longitude = addressData.longitude;
      this.renterInfo.latitude = addressData.latitude;
      this.renterInfo.postCode = addressData.postal_code;
      this.center = { lat: addressData.latitude, lng: addressData.longitude };
    },
    submitPropertyInfo(formName) {
      console.log(this.renterInfo.pictures);
      // this.center = {lat:this.renterInfo.longitude, lng:this.renterInfo.latitude}
      this.$refs[formName].validate((valid) => {
        if (valid && !this.errors.endDate) {
          let mid = localStorage.getItem("id");
          axios
            .post(APIurl + "/property/Property_manage/", {
              // current data binding in the report
              manager_id: parseInt(mid),
              tenant_information:
                this.renterInfo.renterName +
                "|||" +
                this.renterInfo.renterEmail,
              address: this.renterInfo.propertiesAddress,
              postcode: this.renterInfo.postCode.toString(),
              latitude: this.renterInfo.latitude.toString(),
              longitude: this.renterInfo.longitude.toString(),
              last_visit: this.renterInfo.lastVisit,
              rent_start: this.modifyDate(this.renterInfo.rentStartDate),
              rent_end: this.modifyDate(this.renterInfo.rentEndDate),
              // property_Image: "string",

              property_Image: this.renterInfo.pictures,
            })
            .then((response) => {
              if (response.status === 200) {
                let addr = JSON.parse(localStorage.getItem("property_addr"));
                console.log(addr)
                if (addr === null){
                  addr = new Object();
                }
                addr[String(response.data.property_id)] = {
                  formatted_address: this.renterInfo.propertiesAddress,
                  loc: {
                    lng: this.renterInfo.longitude,
                    lat: this.renterInfo.latitude,
                  },
                  pid: response.data.property_id,
                };
                
                localStorage.setItem("property_addr", JSON.stringify(addr));
                ElMessage({
                  showClose: true,
                  message: "Add Property Successfully.",
                  type: "success",
                  center: true,
                });
                this.$router.push("/myproperties");
              }
            }).catch((error) => {
              if (error.response.status === 400) {
                ElMessage({
                  showClose: true,
                  message: "This property already exist,you cannot add this property.",
                  type: "error",
                  center: true,
                });
              }
            });
          // ElMessage({
          //   showClose: true,
          //   message: "Add Property Successfully.",
          //   type: "success",
          //   center: true,
          // });

          // this.$router.push("/myproperties");
        } else {
          // alert("Current Information exists error! Please check Again!")
          ElMessage({
            showClose: true,
            message: "Current Information is invalid! Please check Again!",
            type: "error",
            center: true,
          });
        }
      });
    },
    clearPropertyInfo() {
      (this.renterInfo.renterName = ""),
        (this.renterInfo.renterTel = ""),
        (this.renterInfo.renterEmail = ""),
        (this.renterInfo.propertiesAddress = ""),
        (this.renterInfo.postCode = ""),
        (this.renterInfo.rentStartDate = ""),
        (this.renterInfo.rentEndDate = ""),
        (this.renterInfo.latitude = 0),
        (this.renterInfo.longitude = 0);
      this.center = {
        lat: this.renterInfo.latitude,
        lng: this.renterInfo.longitude,
      };
    },
  },
});
</script>



<style scoped>
.html {
  font-family: "Times New Roman", Times, serif;
}
.property-image-card {
  width: 100%;
  height: 300px;
}
.properties-information {
  height: 200px;
}

.property-info-card {
  display: flex;
  justify-content: center;
}

h3 {
  display: flex;
  justify-content: center;
  font-size: 25px;
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
}

.tenant-info {
  display: flex;
  justify-content: center;
}

.Google-map {
  width: 100%;
  height: 300px;
}

.uploading-img-card {
  display: flex;
  justify-content: center;
  text-align: center;
}

.uploading-blank {
  width: 100%;
  height: 100px;
}

.address-input::-webkit-input-placeholder,
.Teest::-webkit-input-placeholder {
  color: #c0c4cc;
}

.Teest {
  background-color: var(--el-input-background-color, var(--el-color-white));
  background-image: none;
  border-radius: var(--el-input-border-radius, var(--el-border-radius-base));
  border: var(--el-input-border, var(--el-border-base));
  box-sizing: border-box;
  color: var(--el-input-font-color, var(--el-text-color-regular));
  display: inline-block;
  font-size: inherit;
  height: 40px;
  line-height: 40px;
  outline: 0;
  padding: 0 15px;
  width: 100%;
}

.index-container {
  height: 74rem;
}
</style>