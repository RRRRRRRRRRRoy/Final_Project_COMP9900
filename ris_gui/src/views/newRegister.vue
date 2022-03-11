<template>
  <div>
    <el-row justify="center" class="register-page" align="middle">
      <el-card class="register-card" shadow="hover">
        <el-container>
          <el-header height="40%">
            <!-- logo -->
            <el-row justify="center" align="middle"
              ><el-link href="/" :underline="false">
                <img
                  src="../assets/logo1.png"
                  height="80"
                  width="80" /></el-link
            ></el-row>
            <el-row style="height: 30px"></el-row>
            <register-steps :registerStep="registerStep" /> </el-header
          ><el-main>
            <!-- step 0 -->
            <div v-if="registerStep == 0">
              <el-form
                ref="registerForm.forms.f1"
                :model="registerForm.forms.f1"
                :rules="rules1"
              >
                <el-row
                  justify="center"
                  style="color: #365638; font-weight: bold; height: 30px"
                  >TELL US WHO YOU ARE</el-row
                ><!-- select role --><el-form-item prop="role">
                  <el-row justify="center">
                    <select-role
                      :role="registerForm.forms.f1.role"
                      :roleBoxStyle="roleBoxStyle"
                      @changeRole="getRole"
                    /> </el-row></el-form-item
                ><!-- enter name -->
                <el-form-item prop="name"
                  ><el-row justify="center">
                    <el-input
                      v-model="registerForm.forms.f1.name"
                      class="register-input"
                      placeholder="USERNAME"
                    >
                      <template #prefix
                        ><i
                          class="el-input__icon el-icon-user"
                          style="color: #365638; font-weight: bold"
                        ></i></template></el-input></el-row
                ></el-form-item>
                <!-- enter mobile -->
                <el-form-item prop="mobile"
                  ><el-row justify="center">
                    <el-input
                      v-model="registerForm.forms.f1.mobile"
                      class="register-input"
                      placeholder="MOBILE PHONE"
                    >
                      <template #prefix
                        ><i
                          class="el-input__icon el-icon-mobile-phone"
                          style="color: #365638; font-weight: bold"
                        ></i></template
                    ></el-input> </el-row
                ></el-form-item>
                <!-- next step button -->
                <el-row justify="center">
                  <el-button
                    @click="submitRegisterSubform('registerForm.forms.f1')"
                    style="
                      color: #ffffff;
                      background-color: #365638;
                      font-weight: bold;
                    "
                    >NEXT STEP</el-button
                  >
                </el-row>
              </el-form>
            </div>
            <!-- step 1 -->
            <div v-if="registerStep == 1">
              <el-form
                ref="registerForm.forms.f2"
                :model="registerForm.forms.f2"
                :rules="rules2"
                ><el-row
                  justify="center"
                  style="color: #365638; font-weight: bold; height: 30px"
                  >VERIFY YOUR EMAIL</el-row
                >
                <el-form-item prop="email"
                  ><el-row justify="center">
                    <el-popover
                      placement="bottom"
                      :show-arrow="false"
                      :width="220"
                      :offset="0"
                      :visible="
                        registerForm.forms.f2.email !== '' &&
                        !/@/.test(registerForm.forms.f2.email)
                      "
                      trigger="focus"
                    >
                      <template #reference>
                        <el-input
                          v-model="registerForm.forms.f2.email"
                          clearable
                          placeholder="EMAIL"
                          class="register-input"
                          :disabled="registerForm.forms.f2.otcVeri != ''"
                        >
                          <template #prefix
                            ><i
                              class="el-input__icon el-icon-message"
                              style="color: #365638; font-weight: bold"
                            ></i
                          ></template>
                        </el-input>
                      </template>
                      <div v-for="suffix in emailC" :key="suffix">
                        <div
                          style="
                            font-weight: bold;
                            color: #365638;
                            cursor: pointer;
                          "
                          @click="completeEmail(suffix.value)"
                        >
                          {{ registerForm.forms.f2.email }}{{ suffix.value }}
                        </div>
                      </div>
                    </el-popover>
                  </el-row> </el-form-item
                ><!-- send otc button--><el-form-item>
                  <el-row justify="center">
                    <el-button
                      style="
                        width: 100%;
                        color: #ffffff;
                        font-weight: bold;
                        background-color: #365638;
                      "
                      v-if="registerForm.forms.f2.otcVeri == ''"
                      @click="emailVerification"
                    >
                      SEND ONE-TIME CODE
                    </el-button>
                    <el-row v-else style="width: 100%">
                      <el-col :span="13">
                        <el-button
                          style="
                            width: 100%;
                            color: #ffffff;
                            font-weight: bold;
                            background-color: #365638;
                          "
                          @click="changeRegisterEmail"
                          >CHANGE EMAIL
                        </el-button></el-col
                      ><el-col :span="11">
                        <el-button
                          :disabled="resendEmailCD != 0"
                          style="
                            width: 100%;
                            color: #ffffff;
                            font-weight: bold;
                            background-color: #365638;
                          "
                          @click="emailVerification"
                          >RESEND<span v-if="resendEmailCD != 0"
                            >({{ resendEmailCD }}s)</span
                          >
                        </el-button></el-col
                      ></el-row
                    >
                  </el-row></el-form-item
                ><!-- otc input --><el-form-item>
                  <el-row justify="center">
                    <el-input
                      v-model="registerForm.forms.f2.otc"
                      placeholder="ENTER ONE-TIME CODE"
                      :disabled="registerForm.forms.f2.otcVeri == ''"
                      class="register-input"
                      ><template #prefix
                        ><i
                          class="el-input__icon el-icon-key"
                          style="color: #365638; font-weight: bold"
                        ></i></template></el-input></el-row
                ></el-form-item>
                <el-form-item>
                  <el-row justify="center" align="buttom">
                    <el-button-group>
                      <el-button
                        style="
                          color: #ffffff;
                          font-weight: bold;
                          background-color: #365638;
                        "
                        @click="previousRegisterStep"
                      >
                        BACK
                      </el-button>
                      <el-button
                        style="
                          color: #ffffff;
                          font-weight: bold;
                          background-color: #365638;
                        "
                        @click="checkOTC"
                        :disabled="registerForm.forms.f2.otcVeri == ''"
                        >NEXT</el-button
                      ></el-button-group
                    ></el-row
                  ></el-form-item
                ></el-form
              ><el-row style="height: 12px"></el-row>
            </div>
            <!-- step 2 -->
            <div v-if="registerStep == 2">
              <el-form
                ref="registerForm.forms.f3"
                :model="registerForm.forms.f3"
                :rules="rules3"
                ><el-row
                  justify="center"
                  style="color: #365638; font-weight: bold; height: 30px"
                  >SET YOUR PASSWORD</el-row
                >
                <el-form-item prop="password"
                  ><el-row justify="center">
                    <el-popover :show-arrow="false" :width="240" :offset="20">
                      <template #reference>
                        <el-input
                          v-model="registerForm.forms.f3.password"
                          show-password
                          clearable
                          class="register-input"
                          placeholder="PASSWORD"
                        >
                          <template #prefix
                            ><i
                              class="el-input__icon el-icon-key"
                              style="color: #365638; font-weight: bold"
                            ></i
                          ></template> </el-input
                      ></template>
                      <password-tip
                        :password="registerForm.forms.f3.password"
                        :passwordIntensity="passwordIntensity"
                        :textColor="'#365638'"
                      />
                    </el-popover> </el-row
                ></el-form-item>
                <el-form-item prop="repassword"
                  ><el-row justify="center">
                    <el-input
                      v-model="registerForm.forms.f3.repassword"
                      show-password
                      clearable
                      class="register-input"
                      placeholder="COMFIRM PASSWORD"
                      :disabled="passwordIntensity !== 100"
                      ><template #prefix
                        ><i
                          class="el-input__icon el-icon-key"
                          style="color: #365638; font-weight: bold"
                        ></i
                      ></template> </el-input></el-row
                ></el-form-item>
                <el-form-item>
                  <el-row justify="center" align="buttom">
                    <el-button-group>
                      <el-button
                        style="
                          color: #ffffff;
                          font-weight: bold;
                          background-color: #365638;
                        "
                        @click="previousRegisterStep"
                      >
                        BACK
                      </el-button>
                      <el-button
                        style="
                          color: #ffffff;
                          font-weight: bold;
                          background-color: #365638;
                        "
                        @click="register"
                        >NEXT</el-button
                      ></el-button-group
                    ></el-row
                  ></el-form-item
                > </el-form
              ><el-row style="height: 65px"></el-row>
            </div>
            <!-- step 3 -->
            <div v-if="registerStep == 3">
              <el-result title="FINISH!" icon="success" style="color: #365638">
              </el-result>

              <el-row justify="center">
                <el-button @click="registerLogin" class="register-button"
                  >AUTOMATICALLY LOGIN</el-button
                ></el-row
              ><el-row justify="center">
                <el-button @click="toHome" class="register-button"
                  >GO TO HOMEPAGE</el-button
                ></el-row
              >
            </div></el-main
          ><el-footer height="20%" v-if="registerStep < 3"
            ><el-row style="width: 280px" justify="center">
              <span style="font-size: 10px; color: #365638"
                >ALREADY HAVE AN ACCOUNT? &nbsp;</span
              >
              <el-link
                href="/login"
                :underline="false"
                style="font-size: 10px; font-weight: bold; color: #365638"
              >
                SIGN IN
              </el-link>
            </el-row></el-footer
          >
        </el-container></el-card
      ></el-row
    >
  </div>
</template>

<script>
import selectRole from "../components/auth/selectRole.vue";
import emailFormatCheck from "../utils/formValidator/emailFormatCheck.js";
import passwordIntensity from "../utils/formValidator/passwordIntensity";
import telFormatCheck from "../utils/formValidator/telFormatCheck";
import usernameFormatCheck from "../utils/formValidator/usernameFormatCheck.js";
import { emailSuffix } from "../utils/formValidator/emailFormatCheck";
import { APIurl } from "@/http";
import { ElMessage } from "element-plus";
import { ref } from "vue";
import RegisterSteps from "../components/auth/registerSteps.vue";
import PasswordTip from "../components/auth/passwordTip.vue";

export default {
  components: { selectRole, RegisterSteps, PasswordTip },
  data() {
    const checkPassword = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please confirm the password."));
      } else if (value !== this.registerForm.forms.f3.password) {
        callback(new Error("Two different passwords."));
      } else {
        callback();
      }
    };
    const passwordIntensityCheck = (rule, value, callback) => {
      if (value === "") {
        this.passwordIntensity = 0;
        callback(new Error("Please set your password."));
      } else if (value.match(/[\s\'\"]/)) {
        callback(new Error("Space, ' and \" are not permitted."));
      } else {
        this.passwordIntensity = passwordIntensity(value);
        if (this.passwordIntensity !== 100) {
          callback(new Error("Please increase the password intensity."));
        } else callback();
      }
    };
    return {
      emailC: emailSuffix,
      rules1: {
        role: [
          {
            required: true,
            message: "Please select your role.",
            trigger: "blur",
          },
        ],
        name: [
          {
            required: true,
            message: "Please enter your username.",
            trigger: "change",
          },
          {
            validator: usernameFormatCheck,
            trigger: "change",
          },
        ],
        mobile: [
          {
            validator: telFormatCheck,
            trigger: "blur",
          },
        ],
      },
      rules2: {
        email: [
          { validator: emailFormatCheck, trigger: "change" },
          {
            required: true,
            message: "Please enter the email.",
            trigger: "change",
          },
        ],
      },
      rules3: {
        password: [
          {
            validator: passwordIntensityCheck,
            trigger: "change",
          },
        ],
        repassword: [
          {
            validator: checkPassword,
            trigger: "change",
          },
        ],
      },
      nextClick: ref(false),
      resendEmailCD: ref(0),
      passwordIntensity: 0,
      registerStep: 0,
      registerForm: {
        forms: {
          f1: {
            role: "",
            name: "",
            mobile: "",
          },
          f2: {
            email: "",
            otc: "",
            otcVeri: "",
            otcExpire: 0,
          },
          f3: {
            password: "",
            repassword: "",
          },
        },
      },
    };
  },
  methods: {
    getRole(role) {
      this.registerForm.forms.f1.role = role;
    },
    getPassword(password) {
      this.registerForm.forms.f3.password = password;
    },
    submitRegisterSubform(formName) {
      this.nextClick = true;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.registerStep = 1;
        } else {
          return false;
        }
      });
    },
    emailVerification() {
      this.$refs["registerForm.forms.f2"].validate((valid) => {
        if (valid) {
          let form1 = {
            role: this.registerForm.forms.f1.role,
            email: this.registerForm.forms.f2.email,
          };
          this.$axios
            .post(APIurl + "/auth/emailValid", form1)
            .then((response) => {
              if (response.status === 200) {
                this.$axios
                  .post(APIurl + "/email/Validation", {
                    email: this.registerForm.forms.f2.email,
                    require_type: "c",
                  })
                  .then((response) => {
                    if (response.status === 200) {
                      this.registerForm.forms.f2.otcVeri = response.data.v_code;
                      let time = new Date();
                      this.registerForm.forms.f2.otcExpire =
                        time.getTime() + 10 * 60 * 1000; // 10 min
                      this.resendEmailTimer();
                      ElMessage({
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
                ElMessage({
                  showClose: true,
                  message: error.response.data.msg,
                  type: "error",
                  center: true,
                });
              }
            });
        }
      });
    },
    changeRegisterEmail() {
      this.registerForm.forms.f2.otcVeri = "";
      this.registerForm.forms.f2.otc = "";
    },
    checkOTC() {
      let time = new Date();
      if (time.getTime() > this.registerForm.forms.f2.otcExpire) {
        ElMessage({
          showClose: true,
          message: "One-Time Code is expired, please resend.",
          type: "error",
          center: true,
        });
      } else {
        if (
          this.registerForm.forms.f2.otc == this.registerForm.forms.f2.otcVeri
        ) {
          ElMessage({
            showClose: true,
            message: "Email verificated successfully.",
            type: "success",
            center: true,
          });
          this.registerStep = 2;
        } else {
          ElMessage({
            showClose: true,
            message: "Incorrect One-Time Code.",
            type: "error",
            center: true,
          });
        }
      }
    },
    previousRegisterStep() {
      this.registerStep--;
    },
    register() {
      this.$refs["registerForm.forms.f3"].validate((valid) => {
        if (valid) {
          this.$axios
            .post(APIurl + "/auth/register", {
              role: this.registerForm.forms.f1.role,
              username: this.registerForm.forms.f1.name,
              phone: this.registerForm.forms.f1.mobile,
              email: this.registerForm.forms.f2.email,
              password: this.registerForm.forms.f3.password,
            })
            .then((response) => {
              if (response.status === 200) {
                ElMessage({
                  showClose: true,
                  message: "Register successfully.",
                  type: "success",
                  center: true,
                });
                this.registerStep = 3;
              }
            });
        }
      });
    },
    toHome() {
      this.$router.push("/");
    },
    registerLogin() {
      this.$axios
        .post(APIurl + "/auth/login", {
          role: this.registerForm.forms.f1.role,
          email: this.registerForm.forms.f2.email,
          password: this.registerForm.forms.f3.password,
        })
        .then((response) => {
          if (response.status === 200) {
            if (response.data.avatar === "") {
              localStorage.setItem(
                "avatar",
                "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
              );
            } else {
              localStorage.setItem("avatar", response.data.avatar);
            }
            localStorage.setItem("id", response.data.id);
            localStorage.setItem("role", this.registerForm.forms.f1.role);
            localStorage.setItem("Token", response.data.token);
            ElMessage({
              showClose: true,
              message: "Login successfully.",
              type: "success",
              center: true,
            });
            this.$root.logged = true;
            this.$router.push("/");
          }
        });
    },
    completeEmail(row) {
      this.registerForm.forms.f2.email += row;
    },
    resendEmailTimer() {
      this.resendEmailCD = 10;
      var timer = setInterval(() => {
        if (this.resendEmailCD > 0) {
          this.resendEmailCD -= 1;
        } else {
          clearInterval(timer);
        }
      }, 1000);
    },
  },
  computed: {
    roleBoxStyle() {
      return this.nextClick && this.registerForm.forms.f1.role === ""
        ? "#f56c6c"
        : "#365638";
    },
  },
};
</script>

<style scoped>
.register-card {
  width: 360px;
  height: 510px;
  filter: saturate(80%);
  border: solid #365638 3px;
  background-color: white;
  border-radius: 10px;
}

.register-input :deep(input) {
  color: #365638;
  font-weight: bold;
  border: solid #365638;
  height: 40px;
}

.register-input :deep(input::-webkit-input-placeholder) {
  color: #788f77;
}

.register-button {
  width: 100%;
  background-color: #365638;
  color: #ffffff;
  border: none;
  font-weight: bold;
  font-size: 16px;
  margin-top: 15px;
}

.register-page {
  background-image: url("../assets/loginbg1.jpg");
  background-size: cover;
  background-position: center;
  height: 100vh;
}
</style>