<template>
  <div style="margin: 10px; height: 500px">
    <el-header
      style="padding: 0px; border-bottom: solid 1px #c0c4cc; height: 46px"
    >
      <el-row justify="space-between" align="center">
        <span style="font-weight: bold"> My Profile </span>
        <el-row
          justify="space-between"
          style="
            width: 180px;
            border: 1px solid black;
            padding: 3px;
            border-radius: 5px;
          "
        >
          <el-tooltip effect="light" content="Back">
            <i
              class="el-icon-guide"
              @click="cancelEditUser"
              style="cursor: pointer; font-size: 20px"
          /></el-tooltip>
          <el-tooltip effect="light" content="Edit Profile">
            <i
              class="el-icon-user"
              @click="editUser"
              style="cursor: pointer; font-size: 20px" /></el-tooltip
          ><el-tooltip effect="light" content="Change Password">
            <i
              class="el-icon-key"
              @click="editPswd"
              style="cursor: pointer; font-size: 20px" /></el-tooltip
          ><el-tooltip effect="light" content="Change Email">
            <i
              class="el-icon-message"
              @click="editEmail"
              style="cursor: pointer; font-size: 20px" /></el-tooltip
          ><el-tooltip
            effect="light"
            v-if="user.role === 'manager'"
            content="Change Address"
          >
            <i
              class="el-icon-location-information"
              @click="editAddress"
              style="cursor: pointer; font-size: 20px"
          /></el-tooltip>
          <el-tooltip
            effect="light"
            v-if="user.role === 'tenant'"
            content="Edit Property"
          >
            <i
              class="el-icon-house"
              @click="editAddress"
              style="cursor: pointer; font-size: 20px"
          /></el-tooltip>
        </el-row>
      </el-row>
      <el-row v-if="edit === 'profile'"> <i>Modify My Profile</i></el-row>
      <el-row v-if="edit === 'password'"> <i>Change My Password</i></el-row>
      <el-row v-if="edit === 'email'"><i>Change My Email</i></el-row>
      <el-row v-if="edit === 'address' && user.role === 'manager'"
        ><i>Change My Preferred Start Address</i></el-row
      >
      <el-row v-if="edit === 'address' && user.role === 'tenant'"
        ><i>Edit My Property</i>
      </el-row>
    </el-header>
    <el-main style="height: 100%; padding: 0px; margin: 15px">
      <el-row
        v-if="!edit"
        align="middle"
        style="height: 100%; width: 100%"
        justify="center"
      >
        <el-space direction="vertical" alignment="start" fill>
          <el-row justify="space-around" align="middle" style="width: 350px">
            <el-avatar :src="user.avatar" :size="120" />
            <el-descriptions :column="1" size="medium">
              <template #title style="font-size: 20px"
                >{{ user.name }}
              </template>
              <el-descriptions-item>
                <template #label
                  ><i
                    class="el-icon-collection-tag"
                    style="font-weight: bold" /></template
                >{{ user.role }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label
                  ><i
                    class="el-icon-message"
                    style="font-weight: bold" /></template
                >{{ user.email }}
              </el-descriptions-item>
              <el-descriptions-item v-if="user.mobile">
                <template #label
                  ><i
                    class="el-icon-mobile-phone"
                    style="font-weight: bold" /></template
                >{{ user.mobile }}
              </el-descriptions-item>
            </el-descriptions></el-row
          >
          <div v-if="user.role === 'tenant'">
            <el-divider v-if="user.address !== 'null'" />
            <el-descriptions
              :column="1"
              size="medium"
              title="My Property and Manager"
              v-if="user.address !== 'null'"
            >
              <template #extra>
                <el-button type="primary" size="small" @click="editDate = true"
                  >Pick Inspection Day</el-button
                >
                <el-dialog v-model="editDate" width="25%" destroy-on-close>
                  <template #title>
                    <span style="font-weight: bold; font-size: 20px"
                      >Pick Next Acceptable Inspection Day</span
                    >
                  </template>
                  <template #footer>
                    <el-button
                      type="danger"
                      @click="editDate = false"
                      style="width: 45%"
                      plain
                      >Cancel</el-button
                    >
                    <el-button
                      type="success"
                      @click="confirmEditDate"
                      style="width: 45%"
                      plain
                      :disabled="!inspectionDay"
                      >Confirm</el-button
                    >
                  </template>
                  <el-row style="width: 100%">
                    <el-date-picker
                      v-model="inspectionDay"
                      type="date"
                      placeholder="Pick a day"
                      style="width: 100%"
                      value-format="YYYY-MM-DD"
                    /> </el-row
                ></el-dialog>
              </template>
              <el-descriptions-item v-if="user.address !== 'null'">
                <template #label
                  ><i
                    class="el-icon-location-outline"
                    style="font-weight: bold" /></template
                >{{ user.address }}
              </el-descriptions-item>
              <el-descriptions-item v-if="user.m_user_name !== 'null'">
                <template #label
                  ><i
                    class="el-icon-user"
                    style="font-weight: bold" /></template
                >{{ user.m_user_name }}
              </el-descriptions-item>
              <el-descriptions-item v-if="user.m_email !== 'null'">
                <template #label
                  ><i
                    class="el-icon-message"
                    style="font-weight: bold" /></template
                >{{ user.m_email }}
              </el-descriptions-item>
              <el-descriptions-item v-if="user.m_phone !== 'null'">
                <template #label
                  ><i
                    class="el-icon-mobile-phone"
                    style="font-weight: bold" /></template
                >{{ user.m_phone }}
              </el-descriptions-item>
            </el-descriptions>
            <div v-else>
              <el-alert
                style="cursor: pointer; font-size: 20px"
                title="You have not added your property"
                type="warning"
                description="Please click to add your property for the further use."
                show-icon
                :closable="false"
                @click="editAddress"
              />
            </div>
          </div>
          <div v-if="user.role === 'manager'">
            <el-divider v-if="user.start_1 || user.start_2 || user.start_3" />
            <el-descriptions
              :column="1"
              direction="vertical"
              size="medium"
              title="My Preferred Start Locations"
              v-if="user.start_1 || user.start_2 || user.start_3"
            >
              <template #extra
                ><el-button
                  size="mini"
                  type="primary"
                  @click="showMarker = true"
                  >Show in Map</el-button
                ><el-dialog v-model="showMarker" destroy-on-close>
                  <template #title>
                    <span style="font-weight: bold; font-size: 18px"
                      >My Preferred Start Locations</span
                    >&nbsp; &nbsp;<el-button
                      size="mini"
                      @click="editAddress"
                      type="primary"
                      icon="el-icon-edit"
                      circle
                    />
                  </template>
                  <show-markers
                    :places="{
                      1: user.start_1,
                      2: user.start_2,
                      3: user.start_3,
                    }"
                  />
                </el-dialog>
              </template>
              <div v-for="index in 3" :key="index">
                <el-descriptions-item v-if="user[`start_${index}`]">
                  <template #label
                    ><i class="el-icon-location-outline" /><span
                      style="font-weight: bold"
                      >Address {{ index }}</span
                    ></template
                  ><el-row
                    style="width: 100%; font-weight: bold"
                    justify="center"
                    >{{ user[`start_${index}`].formatted_address }}
                  </el-row>
                </el-descriptions-item>
              </div>
            </el-descriptions>
            <div v-else>
              <el-alert
                style="cursor: pointer; font-size: 20px"
                title="Please add your preferred start addresses"
                type="warning"
                description="Please click to add your preferred start addresses for the further use."
                show-icon
                :closable="false"
                @click="editAddress"
              />
            </div>
          </div>
        </el-space>
      </el-row>
      <el-row
        v-else-if="edit === 'profile'"
        justify="center"
        align="middle"
        style="height: 450px"
      >
        <el-space direction="vertical">
          <el-row>Click to change your avatar</el-row>
          <el-row :style="{ 'font-size': '12px', color: avatarType }"
            >(accept file type: .jpg, .png, .jpeg)</el-row
          >
          <el-row :style="{ color: avatarSize, 'font-size': '12px' }"
            >(maximum file size: 2MB)</el-row
          >
          <el-upload
            action="avatarupLoad"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="beforeAvatarUpload"
            accept=".jpg, .png, .jpeg"
            style="
              position: relative;
              overflow: hidden;
              border: dotted;
              border-radius: 50%;
            "
          >
            <el-avatar
              v-if="editUserForm.avatar"
              :src="editUserForm.avatar"
              style="
                display: block;
                width: 120px;
                height: 120px;
                text-align: center;
                alignment: center;
              "
              :size="50"
            />
            <i
              v-else
              class="el-icon-plus"
              style="
                display: block;
                width: 120px;
                height: 120px;
                text-align: center;
                line-height: 120px;
              "
            />
          </el-upload>
          <el-button @click="handleRemove" size="mini">Remove Avatar</el-button>
          <el-row>Update your personal info</el-row>
          <el-form :rules="profileRules" :model="editUserForm" ref="editUser">
            <el-form-item prop="user_name">
              <el-input
                style="width: 100%"
                v-model="editUserForm.user_name"
                prefix-icon="el-icon-user"
                placeholder="Username"
              >
              </el-input>
            </el-form-item>
            <el-form-item prop="phone">
              <el-input
                style="width: 100%"
                v-model="editUserForm.phone"
                prefix-icon="el-icon-mobile-phone"
                placeholder="Mobile Phone"
              />
            </el-form-item>
          </el-form>

          <el-button-group>
            <el-button
              @click="cancelEditUser"
              type="danger"
              round
              plain
              icon="el-icon-arrow-left"
              style="width: 100px"
              >Cancel</el-button
            >
            <el-button
              type="success"
              @click="saveEditUser"
              round
              plain
              style="width: 100px"
              >Save
              <i class="el-icon-arrow-right" /></el-button></el-button-group
        ></el-space>
      </el-row>
      <el-row
        v-else-if="edit === 'password'"
        justify="center"
        align="middle"
        style="height: 450px; width: 350px"
      >
        <el-form
          :model="changePasswordForm"
          :rules="passwordRules"
          ref="changePassword"
        >
          <el-form-item
            prop="password"
            v-if="changePasswordForm.mode === 'change'"
            ><el-row>Enter your current password</el-row
            ><el-row justify="center">
              <el-input
                v-model="changePasswordForm.password"
                show-password
                clearable
                ><template #prefix
                  ><i class="el-input__icon el-icon-key"></i
                ></template>
              </el-input>
            </el-row>
          </el-form-item>
          <el-form-item
            prop="otcCheck"
            v-if="changePasswordForm.mode === 'reset'"
          >
            <el-row>Enter the One-Time Code</el-row
            ><el-row justify="center">
              <el-input
                v-model="changePasswordForm.otcCheck"
                style="width: 200px"
                clearable
                ><template #prefix
                  ><i class="el-input__icon el-icon-key"></i
                ></template>
              </el-input>
              <el-button
                :disabled="changePasswordForm.otcCD > 0"
                plain
                type="primary"
                style="width: 110px"
                @click="resetPassword"
                >Resend<span v-if="changePasswordForm.otcCD"
                  >({{ changePasswordForm.otcCD }}s)</span
                ></el-button
              >
            </el-row>
          </el-form-item>
          <el-form-item prop="new_password"
            ><el-row>Enter your new password</el-row
            ><el-row justify="center">
              <el-popover :show-arrow="false" :width="240" :offset="20">
                <template #reference>
                  <el-input
                    v-model="changePasswordForm.new_password"
                    show-password
                    clearable
                  >
                    <template #prefix
                      ><i class="el-input__icon el-icon-key"></i
                    ></template> </el-input
                ></template>
                <password-tip
                  :password="changePasswordForm.new_password"
                  :passwordIntensity="pIntensity"
                  :textColor="'black'"
                />
              </el-popover> </el-row
          ></el-form-item>
          <el-form-item prop="c_new_password"
            ><el-row>Confirm your new password</el-row
            ><el-row justify="center">
              <el-input
                v-model="changePasswordForm.c_new_password"
                show-password
                clearable
                :disabled="pIntensity !== 100"
                ><template #prefix
                  ><i class="el-input__icon el-icon-key"></i
                ></template> </el-input></el-row></el-form-item
          ><el-form-item>
            <el-row justify="center">
              <el-button-group>
                <el-button
                  @click="cancelEditUser"
                  type="danger"
                  round
                  plain
                  icon="el-icon-arrow-left"
                  style="width: 100px"
                  >Cancel</el-button
                >
                <el-button
                  type="success"
                  @click="submitChangePassword"
                  round
                  plain
                  style="width: 100px"
                  >Submit
                  <i class="el-icon-arrow-right" /></el-button></el-button-group
            ></el-row>
            <el-row justify="center">
              <el-button
                @click="resetPassword"
                round
                type="warning"
                plain
                style="width: 200px"
                v-if="changePasswordForm.mode === 'change'"
              >
                Reset password by email</el-button
              ><el-button
                @click="toChangePassword"
                round
                type="warning"
                plain
                style="width: 200px"
                v-if="changePasswordForm.mode === 'reset'"
              >
                Change password
              </el-button>
            </el-row>
          </el-form-item>
        </el-form>
      </el-row>
      <el-row
        v-else-if="edit === 'email'"
        justify="center"
        align="middle"
        style="height: 450px"
      >
        <el-form
          :model="changeEmailForm"
          :rules="changeEmailRules"
          ref="changeEmailVeri"
        >
          <el-form-item prop="email">
            <el-row>Please enter the new email</el-row>
            <el-popover
              placement="bottom"
              :show-arrow="false"
              :width="220"
              :offset="0"
              :visible="
                changeEmailForm.email !== '' && !/@/.test(changeEmailForm.email)
              "
              trigger="focus"
            >
              <template #reference>
                <el-input
                  v-model="changeEmailForm.email"
                  clearable
                  placeholder="Email"
                  :disabled="changeEmailForm.otc !== ''"
                  prefix-icon="el-icon-message"
                />
              </template>
              <div v-for="suffix in emailSuffix" :key="suffix">
                <div
                  style="cursor: pointer"
                  @click="completeEmail(suffix.value)"
                >
                  {{ changeEmailForm.email }}{{ suffix.value }}
                </div>
              </div>
            </el-popover>
          </el-form-item>
          <el-form-item>
            <el-button
              style="width: 100%"
              v-if="changeEmailForm.otc == ''"
              @click="emailVerification"
              plain
              round
              type="primary"
            >
              Send One-Time Code
            </el-button>
            <el-row v-else style="width: 100%">
              <el-button-group>
                <!-- <el-col :span="13"> -->
                <el-button @click="changeEmail" type="warning" plain round
                  >Change Email
                </el-button>
                <!-- </el-col><el-col :span="11"> -->
                <el-button
                  :disabled="changeEmailForm.otcCD != 0"
                  style="width: 140px"
                  @click="emailVerification"
                  round
                  type="primary"
                  plain
                  >Resend<span v-if="changeEmailForm.otcCD != 0"
                    >({{ changeEmailForm.otcCD }}s)</span
                  >
                </el-button></el-button-group
              >
              <!-- </el-col> -->
            </el-row>
          </el-form-item>
          <el-form-item>
            <el-row>Please enter the One-Time Code</el-row>
            <el-input
              v-model="changeEmailForm.otcCheck"
              prefix-icon="el-icon-key"
              :disabled="changeEmailForm.otc === ''"
            />
          </el-form-item>
          <el-form-item
            ><el-row justify="center">
              <el-button-group>
                <el-button @click="cancelEditUser" type="danger" plain round
                  >Cancel</el-button
                >
                <el-button @click="submitChangeEmail" type="success" plain round
                  >Submit</el-button
                >
              </el-button-group></el-row
            >
          </el-form-item>
        </el-form>
      </el-row>
      <el-row
        v-else-if="edit === 'address' && user.role === 'manager'"
        justify="center"
        align="middle"
        style="height: 450px; width: 100%"
      >
        <el-alert title="Use Formatted Address" type="info" show-icon>
          <slot
            >Please enter the address via Google Maps Autocomplete. Please
            confirm the address via the map and click the button.
          </slot>
        </el-alert>
        <div
          v-for="(value, key) in editAddressForm"
          :key="key"
          style="width: 100%"
        >
          <!-- user[`start_${key}`] -->
          <div style="width: 100%" v-if="key !== 't'">
            <el-row justify="space-between"
              ><span>Address {{ key }}:</span
              ><span
                style="cursor: pointer; color: blue"
                @click="clearAddr(key)"
                >clear</span
              ></el-row
            ><el-row
              justify="center"
              style="font-weight: bold"
              v-if="editAddressForm[key]"
              >{{
                editAddressForm[key].formatted_address.replace(
                  ", Australia",
                  ""
                )
              }}</el-row
            ><el-row justify="center" style="font-weight: bold" v-else
              >NULL</el-row
            >
            <address-input
              :id="key"
              @get-address="getAddress"
              style="width: 100%"
            />
          </div>
        </div>
        <el-row justify="center">
          <el-button-group>
            <el-button @click="cancelEditUser" type="danger" plain round
              >Cancel</el-button
            >
            <el-button @click="submitChangeAddress" type="success" plain round
              >Submit</el-button
            >
          </el-button-group></el-row
        >
      </el-row>
      <el-row
        v-else-if="edit === 'address' && user.role === 'tenant'"
        justify="center"
        align="middle"
        style="height: 450px; width: 100%"
      >
        <el-row style="width: 100%"
          ><el-row>Your current property address is &nbsp;</el-row>
          <el-row justify="center" style="font-size: 20px; font-weight: bold">{{
            user.address
          }}</el-row></el-row
        >
        <el-row style="width: 100%">
          <div>Edit Property Address</div>
          <el-alert title="Use Formatted Address" type="info" show-icon>
            <slot
              >Please enter the address via Google Maps Autocomplete. Please
              confirm the address via the map and click the button.
            </slot>
          </el-alert>
          <address-input id="t" @get-address="getAddress" style="width: 100%" />
        </el-row>
        <el-row style="width: 100%" v-if="editAddressForm.t.formatted_address"
          ><el-row>The formatted address that you want to change to is</el-row
          ><el-row justify="center" style="font-weight: bold; font-size: 20px">
            {{ editAddressForm.t.formatted_address }}</el-row
          ></el-row
        >
        <el-row justify="center">
          <el-button-group>
            <el-button @click="cancelEditUser" type="danger" plain round
              >Cancel</el-button
            >
            <el-button @click="submitChangeAddress" type="success" plain round
              >Submit</el-button
            >
          </el-button-group></el-row
        >
      </el-row>
    </el-main>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox, ElNotification } from "element-plus";
import { APIurl } from "@/http";
import axios from "axios";
import { ref, reactive, onMounted, getCurrentInstance } from "vue";
import usernameFormatCheck from "../utils/formValidator/usernameFormatCheck";
import telFormatCheck from "../utils/formValidator/telFormatCheck";
import passwordIntensity from "../utils/formValidator/passwordIntensity";
import PasswordTip from "../components/auth/passwordTip.vue";
import AddressInput from "./GoogleMaps/addressInput.vue";
import ShowMarkers from "./GoogleMaps/showMarkers.vue";

export default {
  components: { PasswordTip, AddressInput, ShowMarkers },
  setup() {
    const ctx = getCurrentInstance();
    const edit = ref(false);
    const showMarker = ref(false);
    const editUser = () => {
      edit.value = "profile";
    };
    const editEmail = () => {
      edit.value = "email";
    };
    const editPswd = () => {
      edit.value = "password";
    };
    const editAddress = () => {
      edit.value = "address";
    };
    const user = reactive({
      id: localStorage.getItem("id"),
      role: localStorage.getItem("role"),
      avatar: localStorage.getItem("avatar"),
      name: "",
      mobile: "",
      email: "",
      start_1: "",
      start_2: "",
      start_3: "",
      address: "",
      m_user_name: "",
      m_email: "",
      m_phone: "",
    });
    onMounted(() => {
      axios
        .get(
          APIurl +
            "/user/getuser/" +
            localStorage.getItem("role") +
            "/" +
            localStorage.getItem("id")
        )
        .then((response) => {
          let role = localStorage.getItem("role");
          user.name = response.data.name;
          user.email = response.data.email;
          user.mobile = response.data.mobile;
          if (role === "manager") {
            if (response.data.start_one != null) {
              user.start_1 = JSON.parse(response.data.start_one);
              editAddressForm[1] = user.start_1;
            }
            if (response.data.start_two != null) {
              user.start_2 = JSON.parse(response.data.start_two);
              editAddressForm[2] = user.start_2;
            }
            if (response.data.start_three != null) {
              user.start_3 = JSON.parse(response.data.start_three);
              editAddressForm[3] = user.start_3;
            }
            let addresses = {
              1: user.start_1,
              2: user.start_2,
              3: user.start_3,
            };
            let propAddr = response.data.properties;
            for (let i in propAddr) {
              propAddr[i].loc.lat = Number(propAddr[i].loc.lat);
              propAddr[i].loc.lng = Number(propAddr[i].loc.lng);
            }
            localStorage.setItem(
              "property_addr",
              JSON.stringify(response.data.properties)
            );
            localStorage.setItem("start_address", JSON.stringify(addresses));
            if (
              response.data.inspection_plan !== "null" &&
              response.data.inspection_plan !== null
            ) {
              if (
                JSON.parse(response.data.inspection_plan).plan !== "null" &&
                JSON.parse(response.data.inspection_plan).plan !== null
              ) {
                let Iplan = {
                  day: JSON.parse(response.data.inspection_plan).day,
                  plan: JSON.parse(
                    JSON.parse(response.data.inspection_plan).plan
                  ),
                  duration: Number(
                    JSON.parse(response.data.inspection_plan).duration
                  ),
                  inPlan: JSON.parse(
                    JSON.parse(response.data.inspection_plan).inPlan
                  ),
                };
                ctx.emit(
                  "inspection-day",
                  JSON.parse(response.data.inspection_plan).day
                );
                localStorage.setItem("plan", JSON.stringify(Iplan));
              } else {
                ElMessage({
                  message: "Your previous plan is expired.",
                  center: true,
                  showClose: true,
                });
                localStorage.setItem("plan", null);
              }
            } else {
              localStorage.setItem("plan", null);
            }
          } else {
            if (response.data.inspection_day !== "null") {
              ctx.emit("inspection-day", response.data.inspection_day);
            }
            user.address = response.data.address;
            user.m_user_name = response.data.m_user_name;
            user.m_email = response.data.m_email;
            user.m_phone = response.data.m_phone;
          }
          editUserForm.user_name = user.name;
          editUserForm.phone = user.mobile;
        });
    });
    //--------------------    edit user profile   --------------------//
    const profileRules = {
      user_name: [{ validator: usernameFormatCheck, trigger: "change" }],
      phone: [{ validator: telFormatCheck, trigger: "change" }],
    };
    const cancelEditUser = function () {
      window.location.reload();
    };
    const editUserForm = reactive({
      user_name: user.name,
      phone: user.mobile,
      user_role: user.role,
      avatar: user.avatar,
    });
    // edit user avatar
    const avatarType = ref("black");
    const avatarSize = ref("black");
    const beforeAvatarUpload = (file, filelist) => {
      const isLt2M = file.size / 1024 / 1024 < 2;
      const isImg = ["image/jpg", "image/png", "image/jpeg"].includes(
        file.raw.type
      );
      if (isLt2M && isImg) {
        avatarType.value = "black";
        avatarSize.value = "black";
        var reader = new FileReader();
        reader.readAsDataURL(file.raw);
        reader.onload = () => {
          editUserForm.avatar = reader.result;
        };
      } else {
        editUserForm.avatar = "";
        if (!isLt2M) {
          avatarSize.value = "red";
        }
        if (!isImg) {
          avatarType.value = "red";
        }
      }
    };
    const handleRemove = () => {
      editUserForm.avatar = "";
    };
    const saveEditUser = function () {
      ctx.refs["editUser"].validate((valid) => {
        if (valid) {
          axios
            .patch(APIurl + "/user/user_default/" + user.id, editUserForm)
            .then((response) => {
              if (response.status === 200) {
                edit.value = false;
                user.name = editUserForm.user_name;
                user.mobile = editUserForm.phone;
                if (editUserForm.avatar) {
                  localStorage.setItem("avatar", editUserForm.avatar);
                  user.avatar = editUserForm.avatar;
                } else {
                  localStorage.setItem(
                    "avatar",
                    "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
                  );
                  user.avatar =
                    "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png";
                }
                window.location.reload();
                ElNotification({
                  showClose: true,
                  center: true,
                  message: "Edit successfully",
                  type: "success",
                  customClass: "notification",
                });
              }
            });
        } else {
          return false;
        }
      });
    };
    //----------------------   change password   ---------------------//
    const changePasswordForm = reactive({
      mode: "change",
      otc: "",
      otcCheck: "",
      otcCD: 0,
      otxExpire: 0,
      password: "",
      new_password: "",
      c_new_password: "",
    });
    const pIntensity = ref(0);
    const startTimer = () => {
      changePasswordForm.otcCD = 10;
      var timer = setInterval(() => {
        if (changePasswordForm.otcCD > 0) {
          changePasswordForm.otcCD -= 1;
        } else {
          clearInterval(timer);
        }
      }, 1000);
    };
    const checkPassword = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please confirm the password."));
      } else if (value !== changePasswordForm.new_password) {
        callback(new Error("Two different passwords."));
      } else {
        callback();
      }
    };
    const passwordIntensityCheck = (rule, value, callback) => {
      if (value === "") {
        pIntensity.value = 0;
        callback(new Error("Please set your password."));
      } else if (value.match(/[\s\'\"]/)) {
        callback(new Error("Space, ' and \" are not permitted."));
      } else {
        pIntensity.value = passwordIntensity(value);
        if (pIntensity.value !== 100) {
          callback(new Error("Please increase the password intensity."));
        } else callback();
      }
    };
    const passwordRules = {
      password: [
        {
          required: true,
          message: "Please enter the password.",
          trigger: "blur",
        },
      ],
      otcCheck: [
        { required: true, message: "Please enter the code.", trigger: "blur" },
      ],
      new_password: [{ validator: passwordIntensityCheck, trigger: "change" }],
      c_new_password: [{ validator: checkPassword, trigger: "blur" }],
    };
    const submitChangePassword = () => {
      ctx.refs["changePassword"].validate((valid) => {
        if (valid) {
          let time = new Date();
          if (
            changePasswordForm.otxExpire > 0 &&
            changePasswordForm.otxExpire < time.getTime()
          ) {
            ElNotification({
              showClose: true,
              message: "One-Time Code Expired, please resend.",
              type: "error",
              offset: 10,
              position: "bottom-right",
            });
          } else {
            if (changePasswordForm.otcCheck === changePasswordForm.otc) {
              axios
                .patch(APIurl + "/user/user_password/" + user.id, {
                  user_role: user.role,
                  new_password: changePasswordForm.new_password,
                  old_password: changePasswordForm.password,
                  mode: changePasswordForm.mode,
                })
                .then((response) => {
                  if (response.status === 200) {
                    ElMessageBox.alert(
                      "Change password successfully, please login again.",
                      "successfully",
                      {
                        type: "success",
                        showClose: false,
                        confirmButtonText: "OK",
                        center: true,
                      }
                    ).then(() => {
                      localStorage.clear();
                      sessionStorage.clear();
                      window.location.reload();
                    });
                  }
                })
                .catch((error) => {
                  if (error.response.status === 400) {
                    ElNotification({
                      showClose: true,
                      message: "Incorrect current password.",
                      type: "error",
                      offset: 10,
                      position: "bottom-right",
                    });
                  }
                });
            } else {
              ElNotification({
                showClose: true,
                message: "Incorrect One-Time Code.",
                type: "error",
                offset: 10,
                position: "bottom-right",
              });
            }
          }
        } else {
          return false;
        }
      });
    };
    //----------------------   reset password   ------------------------//
    const toChangePassword = () => {
      changePasswordForm.mode = "change";
      changePasswordForm.otc = "";
      changePasswordForm.otcCheck = "";
    };
    const resetPassword = () => {
      axios
        .post(APIurl + "/email/Validation", {
          email: user.email,
          require_type: "r",
        })
        .then((response) => {
          if (response.status === 200) {
            let time = new Date();
            changePasswordForm.otc = response.data.v_code;
            ElNotification({
              showClose: true,
              message: "One-Time Code has been sent.",
              type: "success",
              offset: 10,
              position: "bottom-right",
              customClass: "notification",
            });
            changePasswordForm.otxExpire = time.getTime() + 10 * 60 * 1000;
            startTimer();
            changePasswordForm.mode = "reset";
          }
        });
    };
    //----------------------    change email     ------------------------//
    const changeEmailForm = reactive({
      email: "",
      otc: "",
      otcCheck: "",
      otcCD: 0,
      otcExpire: 0,
    });
    const changeEmailRules = {
      email: [
        {
          required: true,
          message: "Please enter your email.",
          trigger: "change",
        },
        {
          type: "email",
          message: "Invalid email format.",
          trigger: "change",
        },
      ],
    };
    const emailSuffix = [
      { value: "@gmail.com" },
      { value: "@yahoo.com" },
      { value: "@hotmail.com" },
      { value: "@icloud.com" },
      { value: "@aol.com" },
      { value: "@outlook.com" },
    ];
    const completeEmail = (row) => {
      changeEmailForm.email += row;
    };
    const resendEmailTimer = () => {
      changeEmailForm.otcCD = 10;
      var timer = setInterval(() => {
        if (changeEmailForm.otcCD > 0) {
          changeEmailForm.otcCD -= 1;
        } else {
          clearInterval(timer);
        }
      }, 1000);
    };
    const changeEmail = () => {
      changeEmailForm.otc = "";
      changeEmailForm.otcCheck = "";
      changeEmailForm.otcExpire = 0;
    };
    const emailVerification = () => {
      ctx.refs["changeEmailVeri"].validate((valid) => {
        if (valid) {
          if (changeEmailForm.email !== user.email) {
            let form1 = {
              role: user.role,
              email: changeEmailForm.email,
            };
            axios
              .post(APIurl + "/auth/emailValid", form1)
              .then((response) => {
                if (response.status === 200) {
                  axios
                    .post(APIurl + "/email/Validation", {
                      email: changeEmailForm.email,
                      require_type: "e",
                    })
                    .then((response) => {
                      if (response.status === 200) {
                        changeEmailForm.otc = response.data.v_code;
                        let time = new Date();
                        changeEmailForm.otcExpire =
                          time.getTime() + 10 * 60 * 1000; // 10 min
                        resendEmailTimer();
                        ElNotification({
                          showClose: true,
                          message: "One-Time Code has been sent.",
                          type: "success",
                          center: true,
                        });
                      }
                    });
                }
              })
              .catch((error) => {
                if (error.response.status === 400) {
                  ElNotification({
                    showClose: true,
                    message: error.response.data.msg,
                    type: "error",
                    center: true,
                  });
                }
              });
          } else {
            ElNotification({
              showClose: true,
              message: "Same email address as now.",
              type: "error",
              offset: 10,
            });
          }
        }
      });
    };
    const submitChangeEmail = () => {
      let time = new Date();
      if (
        changeEmailForm.otcExpire > 0 &&
        time.getTime() > changeEmailForm.otcExpire
      ) {
        ElMessage({
          showClose: true,
          message: "One-Time Code is expired.",
          type: "error",
          center: true,
        });
      } else {
        if (changeEmailForm.otc === changeEmailForm.otcCheck) {
          axios
            .patch(APIurl + "/user/user_email/" + user.id, {
              user_role: user.role,
              new_email: changeEmailForm.email,
            })
            .then((response) => {
              if (response.status === 200) {
                ElMessageBox.alert(
                  "Change email successfully, please login again.",
                  "successfully",
                  {
                    type: "success",
                    showClose: false,
                    confirmButtonText: "OK",
                    center: true,
                  }
                ).then(() => {
                  localStorage.clear();
                  sessionStorage.clear();
                  window.location.reload();
                });
              }
            });
        } else {
          ElNotification({
            showClose: true,
            message: "Incorrect One-Time Code.",
            type: "error",
            center: true,
            customClass: "notification",
          });
        }
      }
    };
    // ----------------------  change address -------------------------- //
    const editAddressForm = reactive({
      1: user.start_1,
      2: user.start_2,
      3: user.start_3,
      t: user.address,
    });
    const getAddress = (location, id) => {
      editAddressForm[id] = location;
    };
    const clearAddr = (key) => {
      editAddressForm[key] = "";
    };
    const submitChangeAddress = () => {
      let submitChangeAddressForm = {
        user_role: user.role,
      };
      if (user.role === "manager") {
        // if (editAddressForm[1]) {
          submitChangeAddressForm[1] = JSON.stringify(editAddressForm[1]);
        // }
        // if (editAddressForm[2]) {
          submitChangeAddressForm[2] = JSON.stringify(editAddressForm[2]);
        // }
        // if (editAddressForm[3]) {
          submitChangeAddressForm[3] = JSON.stringify(editAddressForm[3]);
        // }
      } else {
        if (editAddressForm.t) {
          submitChangeAddressForm[1] = editAddressForm.t.formatted_address;
        }
      }
      if (
        (user.role === "manager" &&
          (editAddressForm[1] || editAddressForm[2] || editAddressForm[3])) ||
        (user.role === "tenant" && editAddressForm.t)
      ) {
        axios
          .post(
            APIurl + "/user/user_address/" + user.id,
            submitChangeAddressForm
          )
          .then((response) => {
            if (response.status === 200) {
              ElNotification({
                showClose: true,
                center: true,
                message: "Edit Profile Address Successfully",
                type: "success",
                customClass: "notification",
              });
              window.location.reload();
            }
          })
          .catch((error) => {
            if (error.response.status === 404) {
              ElNotification({
                showClose: true,
                center: true,
                message:
                  "The address does not exist, please contact your manager.",
                type: "error",
                customClass: "notification",
              });
            }
          });
      } else {
        ElNotification({
          showClose: true,
          center: true,
          message: "No Addresses Entered",
          type: "info",
          customClass: "notification",
        });
      }
    };
    // ----------------------- change inspection time  -----------------//
    const editDate = ref(false);
    const inspectionDay = ref(null);
    const confirmEditDate = () => {
      let editDateForm = { day: inspectionDay.value, id: user.id };
      axios
        .post(APIurl + "/email/t_inspection", editDateForm)
        .then((response) => {
          if (response.status === 200) {
            ElMessage({
              showClose: true,
              center: true,
              message: "Pick Inspection Date Successfully.",
              type: "success",
            });
            editDate.value = false;
          }
        });
    };
    return {
      ctx,
      user,
      editUserForm,
      changePasswordForm,
      edit,
      editUser,
      editEmail,
      editPswd,
      editAddress,
      cancelEditUser,
      saveEditUser,
      avatarType,
      avatarSize,
      beforeAvatarUpload,
      handleRemove,
      profileRules,
      passwordRules,
      startTimer,
      checkPassword,
      passwordIntensity,
      passwordIntensityCheck,
      passwordIntensity,
      pIntensity,
      submitChangePassword,
      resetPassword,
      toChangePassword,
      PasswordTip,
      changeEmailForm,
      changeEmailRules,
      completeEmail,
      resendEmailTimer,
      emailVerification,
      submitChangeEmail,
      emailSuffix,
      changeEmail,
      editAddressForm,
      submitChangeAddress,
      inspectionDay,
      getAddress,
      editDate,
      confirmEditDate,
      clearAddr,
      showMarker,
    };
  },
};
</script>

<style scoped>
.edit-address {
  width: 100%;
  height: 38px;
  padding: 0 15px;
  border-radius: 5px;
  border: 1px solid #c0c4cc;
}

.edit-address:focus {
  outline: none;
  border: 1px solid #409eff;
}

.edit-address::-webkit-input-placeholder {
  color: #c0c4cc;
  font-size: 16px;
}

.notification {
  color: red;
}
</style>