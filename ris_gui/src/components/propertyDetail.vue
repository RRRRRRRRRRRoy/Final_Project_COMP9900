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
            >
              <h3>Property Picture</h3>
              <div v-if="!editFlag">
                <el-row type="flex" justify="center" v-if="editImageBuffer.length">
                  <el-col>
                    <el-carousel height="400px" style="width: 1000px">
                      <div v-for="item in editImageBuffer" :key="item">
                        <el-carousel-item>
                          <img class="property-image" :src="item" />
                        </el-carousel-item>
                      </div>
                    </el-carousel>
                  </el-col>
                </el-row>
                <div v-else>
                  <el-space direction="vertical" :size="30">
                    <h4>You did not upload any pictures for this property</h4>
                    <el-row justify="center"
                      ><el-button @click="modify" round plain
                        >Modify Property Detail</el-button
                      ></el-row
                    ></el-space
                  >
                </div>
                <!-- edit pictures -->
              </div>
              <div v-else>
                <el-space direction="vertical" :size="40">
                  <el-row justify="center">Click the picture to delete.</el-row>
                  <el-row type="flex" justify="center">
                    <div v-for="(value, key) in editImageBuffer" :key="key">
                      <div v-if="value">
                        <img
                          class="property-image-edit"
                          :src="value"
                          @click="deleteImage(key)"
                        />
                      </div>
                    </div>
                    <!-- <div v-for="i in addImageQuota" :key="i"> -->
                    <el-upload
                      v-if="addImageQuota"
                      action="xxx"
                      :auto-upload="false"
                      :on-change="handlePictureChange"
                      class="uploader"
                      accept=".jpg, .png, .jpeg"
                    >
                      <i
                        class="el-icon-plus"
                        style="
                          text-align: center;
                          height: 140px;
                          width: 140px;
                          margin-top: 60px;
                        "
                      />
                    </el-upload>
                    <!-- </div> -->
                  </el-row></el-space
                >
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-row><br /></el-row>
        <el-row justify="center">
          <el-col :span="21">
            <el-card class="property-info-card">
              <h3>Property information</h3>
              <br />
              <el-row type="flex" class="properties-infor" justify="center">
                <el-col :span="24">
                  <el-form
                    class="properties-information"
                    :rules="rules"
                    :model="renterInfo"
                    ref="renterInfo"
                  >
                    <el-col>
                      <template v-if="editFlag">
                        <el-form-item label="Renter Name:" prop="renterName">
                          <el-input
                            v-model="renterInfo.renterName"
                            placeholder="Renter Name"
                            clearable
                          />
                        </el-form-item>
                      </template>
                      <template v-else>
                        <p>Name: {{ this.renterInfo.renterName }}</p>
                        <br />
                      </template>

                      <template v-if="editFlag">
                        <el-form-item label="Renter Email:" prop="renterEmail">
                          <el-input
                            v-model="renterInfo.renterEmail"
                            placeholder="Renter Email Address"
                            type="email"
                            clearable
                          />
                        </el-form-item>
                      </template>
                      <template v-else>
                        <p>E-mail: {{ this.renterInfo.renterEmail }}</p>
                        <br />
                      </template>

                      <template v-if="editFlag">
                        <el-form-item label="Address:" prop="propertiesAddress">
                          <vue-google-autocomplete
                            ref="ChangePropertyAddress"
                            id="map"
                            class="Teest address-input"
                            classname="form-control"
                            :placeholder="renterInfo.propertiesAddress"
                            v-model="address"
                            v-on:placechanged="getAddressPrediction"
                            country="au"
                          >
                          </vue-google-autocomplete>
                        </el-form-item>
                      </template>
                      <template v-else>
                        <p>Address: {{ this.renterInfo.propertiesAddress }}</p>
                      </template>
                    </el-col>
                    <el-col>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</el-col>
                    <el-col>
                      <template v-if="editFlag">
                        <el-form-item
                          label="Property Postcode:"
                          prop="postCode"
                        >
                          <el-input
                            v-model="renterInfo.postCode"
                            placeholder="Properties Postcode"
                            clearable
                          />
                        </el-form-item>
                      </template>
                      <template v-else>
                        <p>Postcode: {{ this.renterInfo.postCode }}</p>
                        <br />
                      </template>

                      <template v-if="editFlag">
                        <el-form-item
                          label="Rent Start Date:"
                          prop="rentStartDate"
                        >
                          <el-date-picker
                            @change="modifyDate(renterInfo.rentStartDate)"
                            v-model="renterInfo.rentStartDate"
                            type="date"
                            placeholder="Select Start Date"
                            style="width: 100%"
                          />
                          <!-- <el-input
                          v-model="renterInfo.postCode"
                          placeholder="Properties Postcode"
                          clearable
                        /> -->
                        </el-form-item>
                      </template>
                      <template v-else>
                        <p>Start Date: {{ this.renterInfo.rentStartDate }}</p>
                        <br />
                      </template>

                      <template v-if="editFlag">
                        <el-form-item label="Rent End Date:" prop="rentEndDate">
                          <el-date-picker
                            @change="modifyDate(renterInfo.rentEndDate)"
                            @blur="dateSequenceCheck"
                            v-model="renterInfo.rentEndDate"
                            type="date"
                            placeholder="Select End Date"
                            style="width: 100%"
                          >
                          </el-date-picker>
                          <div
                            class="el-form-item__error"
                            v-if="errors.endDate"
                          >
                            Invalid Rental End Date.
                          </div>
                        </el-form-item>
                      </template>
                      <template v-else>
                        <p>End Date: {{ this.renterInfo.rentEndDate }}</p>
                      </template>
                    </el-col>
                  </el-form>
                </el-col>
              </el-row>
              <el-row type="flex" justify="center">
                <template v-if="!editFlag">
                  <el-button
                    v-if="editFlag"
                    type="primary"
                    round
                    @click="showLocation()"
                    style="font-family: 'Times New Roman', Times, serif"
                  >
                    Show location
                  </el-button>
                  <div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>
                  <el-button
                    type="success"
                    round
                    @click="modify()"
                    style="font-family: 'Times New Roman', Times, serif"
                  >
                    Modify Information
                  </el-button>
                </template>
                <template v-else>
                  <el-button
                    type="success"
                    round
                    @click="UpdatingInformation('renterInfo')"
                    style="font-family: 'Times New Roman', Times, serif"
                  >
                    Update Information
                  </el-button>
                  <div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>
                  <el-button
                    type="danger"
                    round
                    @click="cancelUpdate()"
                    style="font-family: 'Times New Roman', Times, serif"
                  >
                    Cancel Update
                  </el-button>
                </template>
              </el-row>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <el-row><br /></el-row>
      <div>
        <el-row type="flex" class="properties-location" justify="center">
          <el-col :span="21">
            <el-card class="box-card" justify="center">
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
import { GoogleMap, Marker } from "vue3-google-map";
import AddressAnalyzer from "../utils/AddressAnalyzer.js";
import emailFormatCheck from "../utils/formValidator/emailFormatCheck.js";
import postCodeCheck from "../utils/formValidator/postCodeCheck.js";
import axios from "axios";
import moment from "moment";
import { APIurl, Testurl } from "@/http";
import { ElMessage } from "element-plus";
import VueGoogleAutocomplete from "vue-google-autocomplete";

export default {
  components: { GoogleMap, Marker, VueGoogleAutocomplete },
  mounted() {
    this.$axios
      .get(APIurl + "/property/getprop/" + this.$route.query.id)
      .then((response) => {
        if (response.status === 200) {
          let data = response.data.p_info;
          this.renterInfo.renterName = data.t_info.split("|||")[0];
          this.renterInfo.renterEmail = data.t_info.split("|||")[1];
          this.renterInfo.propertiesAddress = data.address;
          this.renterInfo.postCode = data.postcode;
          this.renterInfo.lastVisit = data.last_visit;
          this.renterInfo.rentStartDate = data.rent_start;
          this.renterInfo.rentEndDate = data.rent_end;
          this.renterInfo.longitude = data.longitude;
          this.renterInfo.latitude = data.latitude;
          if (data.property_Image) {
            let img = JSON.parse(data.property_Image);
            for (let key in img) {
              if (img[key]) {
                this.editImageBuffer.push(img[key]);
              }
            }
          }
          console.log(this.editImageBuffer)
          this.center = {
            lat: Number(this.renterInfo.latitude),
            lng: Number(this.renterInfo.longitude),
          };
        }
      });
  },
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
        this.renterInfo.rentStartDate = moment(
          this.renterInfo.rentStartDate
        ).format("YYYY-MM-DD");
        this.renterInfo.rentEndDate = moment(
          this.renterInfo.rentEndDate
        ).format("YYYY-MM-DD");
      }
    },
    addImageQuota() {
      return 5 - this.editImageBuffer.length;
    },
  },
  data() {
    return {
      editFlag: false,
      center: { lat: 0, lng: 0 },
      dialogImageUrl: "",
      dialogVisible: false,
      rulerChecker: true,
      errors: {
        endDate: "",
      },
      // address: JSON.parse(localStorage.getItem("p_detail")).address,
      address: null,
      renterInfo: {
        renterName: null,
        renterEmail: null,
        propertiesAddress: null,
        postCode: null,
        lastVisit: null,
        rentStartDate: null,
        rentEndDate: null,
        longitude: null,
        latitude: null,
        p_id: this.$route.query.id,
        property_Image: null,
      },
      editImageBuffer: [],
      // renterInfo: {
      //   renterName: JSON.parse(localStorage.getItem("p_detail")).t_info.split(
      //     "|||"
      //   )[0],
      //   renterEmail: JSON.parse(localStorage.getItem("p_detail")).t_info.split(
      //     "|||"
      //   )[1],
      //   propertiesAddress: JSON.parse(localStorage.getItem("p_detail")).address,
      //   postCode: JSON.parse(localStorage.getItem("p_detail")).postcode,
      //   lastVisit: JSON.parse(localStorage.getItem("p_detail")).last_visit,
      //   rentStartDate: JSON.parse(localStorage.getItem("p_detail")).rent_start,
      //   rentEndDate: JSON.parse(localStorage.getItem("p_detail")).rent_end,
      //   longitude: JSON.parse(localStorage.getItem("p_detail")).longitude,
      //   latitude: JSON.parse(localStorage.getItem("p_detail")).latitude,
      //   p_id: JSON.parse(localStorage.getItem("p_detail")).p_id,
      //   // property_Image: JSON.parse(
      //   //   JSON.parse(localStorage.getItem("p_detail")).property_Image
      //   // ),
      // },
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
  methods: {
    modify() {
      this.editFlag = !this.editFlag;
    },
    showLocation() {
      let current_address = this.renterInfo.propertiesAddress;
      if (current_address != "") {
        AddressAnalyzer(current_address);
        this.renterInfo.latitude = window.lat_lng.lat;
        this.renterInfo.longitude = window.lat_lng.lng;
        this.renterInfo.latitude = localStorage.getItem("lat");
        this.renterInfo.longitude = localStorage.getItem("lng");
        console.log(
          "This is properties lat",
          parseFloat(this.renterInfo.latitude)
        );
        console.log(
          "This is properties lng",
          parseFloat(this.renterInfo.longitude)
        );
        this.center = {
          lat: parseFloat(this.renterInfo.latitude),
          lng: parseFloat(this.renterInfo.longitude),
        };
      } else {
        ElMessage({
          showClose: true,
          message: "The Address is empty.",
          type: "error",
          center: true,
        });
      }
    },
    getAddressPrediction(addressData, placeResultData, id) {
      this.renterInfo.propertiesAddress = addressData;
      this.renterInfo.propertiesAddress = placeResultData.formatted_address;
      console.log(placeResultData.formatted_address);
      console.log(addressData.latitude);
      console.log(addressData.longitude);
      this.renterInfo.longitude = addressData.longitude;
      this.renterInfo.latitude = addressData.latitude;
      this.renterInfo.postCode = addressData.postal_code;
      this.center = { lat: addressData.latitude, lng: addressData.longitude };
    },
    UpdatingInformation(formName) {
      // console.log()
      this.$refs[formName].validate((valid) => {
        if (valid && !this.errors.endDate) {
          let images = new Object();
          for (let i = 0; i < this.editImageBuffer.length; i += 1) {
            images[i] = this.editImageBuffer[i];
          }
          console.log(images);
          console.log(this.renterInfo.p_id);
          let form = {
            // current data binding in the report
            property_id: Number(this.renterInfo.p_id),
            tenant_information:
              this.renterInfo.renterName + "|||" + this.renterInfo.renterEmail,
            address: this.renterInfo.propertiesAddress,
            postcode: this.renterInfo.postCode,
            latitude: "" + this.renterInfo.latitude,
            longitude: "" + this.renterInfo.longitude,
            last_visit: this.renterInfo.lastVisit,
            rent_start: this.renterInfo.rentStartDate,
            rent_end: this.renterInfo.rentEndDate,
            property_Image: images,
            // property_Image: '',
          };
          console.log(form);
          axios
            .patch(
              APIurl + `/property/Property_modify/`,
              // {
              //   // current data binding in the report
              //   property_id: Number(this.renterInfo.p_id),
              //   tenant_information:
              //     this.renterInfo.renterName +
              //     "|||" +
              //     this.renterInfo.renterEmail,
              //   address: this.renterInfo.propertiesAddress,
              //   postcode: this.renterInfo.postCode,
              //   latitude: "" + this.renterInfo.latitude,
              //   longitude: "" + this.renterInfo.longitude,
              //   last_visit: this.renterInfo.lastVisit,
              //   rent_start: this.renterInfo.rentStartDate,
              //   rent_end: this.renterInfo.rentEndDate,
              //   property_Image: images,
              //   // property_Image: '',
              // }
              form
            )
            .then((response) => {
              if (response.status === 200) {
                ElMessage({
                  showClose: true,
                  message: "Update Property Information Successfully.",
                  type: "success",
                  center: true,
                });
                let p_addr = JSON.parse(localStorage.getItem("property_addr"));
                p_addr[this.renterInfo.p_id] = {
                  loc: {
                    lng: this.renterInfo.longitude,
                    lat: this.renterInfo.latitude,
                  },
                  formatted_address: this.renterInfo.propertiesAddress,
                  pid: this.renterInfo.p_id,
                };
                localStorage.setItem("property_addr", JSON.stringify(p_addr));
                window.location.reload();
              }
            })
            .catch((error) => {
              if (error.response.status === 400) {
                ElMessage({
                  showClose: true,
                  message:
                    "This property already exist, you cannot add this property.",
                  type: "error",
                  center: true,
                });
              }
            });
          // this.editFlag = false;
        } else {
          ElMessage({
            showClose: true,
            message: "Information is invalid! Please Change it!",
            type: "error",
            center: true,
          });
        }
      });
    },
    cancelUpdate() {
      this.editFlag = !this.editFlag;
      location.reload();
    },
    modifyDate(Date) {
      return moment(Date).format("YYYY-MM-DD");
    },
    handlePictureChange(file) {
      const isLt2M = file.size / 1024 / 1024 < 2;
      const isImg = ["image/jpg", "image/png", "image/jpeg"].includes(
        file.raw.type
      );
      if (isLt2M && isImg) {
        var reader = new FileReader();
        reader.readAsDataURL(file.raw);
        reader.onload = () => {
          this.editImageBuffer.push(reader.result);
        };
        console.log(this.editImageBuffer);
      } else {
        ElMessage({
          message:
            "Picture should be less than 2MB and in .jpg, .png or .jpeg format.",
          type: "error",
          center: true,
        });
      }
    },
    deleteImage(key) {
      this.editImageBuffer.splice(key, 1);
      console.log(this.editImageBuffer);
    },
  },
};
</script>

<style scoped>
.property-image {
  object-fit: contain;
  object-position: center;
  width: 1000px;
  height: 400px;
}

.property-image-edit {
  cursor: pointer;
  object-fit: scale-down;
  object-position: center;
  width: 140px;
  height: 140px;
}

.uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 140px;
  height: 140px;
}

.html {
  font-family: "Times New Roman", Times, serif;
}
/* .property-image-card {
  width: 100%;
  height: 1000px;
} */
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

.font-format p {
  font-size: 10px;
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
  height: 90rem;
}
</style>