<template>
  <div>
    <el-row justify="center">
      <el-card style="width: 600px" shadow="hover">
        <el-container>
          <el-header>Register<el-divider></el-divider></el-header>
          <el-steps :active="registerStep" align-center finish-status="success">
            <el-step title="Basic Info"> </el-step>
            <el-step title="Verification"></el-step>
            <el-step title="Password"></el-step>
            <el-step title="Complete"></el-step> </el-steps
          ><br />
          <!--  -->
          <div v-if="registerStep == 0">
            <el-form
              ref="registerForm.forms.f1"
              :model="registerForm.forms.f1"
              :rules="rules1"
            >
              <el-divider> Select a kind of account </el-divider>
              <el-row justify="center">
                <el-form-item prop="role">
                  <el-radio-group v-model="registerForm.forms.f1.role">
                    <el-radio-button label="manager">Manager</el-radio-button>
                    <el-radio-button label="tenant">Tenant</el-radio-button>
                  </el-radio-group></el-form-item
                ></el-row
              >
              <el-divider> Enter your information </el-divider>
              <el-row justify="center">
                <el-form-item prop="name">
                  <el-input
                    v-model="registerForm.forms.f1.name"
                    style="width: 350px"
                    prefix-icon="el-icon-user"
                    placeholder="Username"
                  /> </el-form-item
              ></el-row>
              <el-row justify="center">
                <el-form-item prop="mobile">
                  <el-input
                    v-model="registerForm.forms.f1.mobile"
                    style="width: 350px"
                    prefix-icon="el-icon-mobile"
                    placeholder="Mobile phone"
                  /> </el-form-item
              ></el-row>
              <el-divider></el-divider>
              <el-row justify="center">
                <el-button
                  @click="submitRegisterSubform('registerForm.forms.f1')"
                  icon="el-icon-arrow-right"
                  round
                  type="primary"
                  style="width: 160px"
              /></el-row>
            </el-form>
          </div>
          <!--  -->
          <div v-if="registerStep == 1">
            <el-form
              ref="registerForm.forms.f2"
              :model="registerForm.forms.f2"
              :rules="rules2"
            >
              <el-divider>Enter your email address</el-divider
              ><el-row justify="center">
                <el-form-item prop="email">
                  <el-input
                    v-model="registerForm.forms.f2.email"
                    :disabled="registerForm.forms.f2.otcVeri != ''"
                    style="width: 350px"
                    prefix-icon="el-icon-message"
                    clearable
                  /> </el-form-item></el-row
              ><el-row justify="center">
                <el-button
                  v-if="registerForm.forms.f2.otcVeri == ''"
                  @click="emailVerification"
                  style="width: 350px"
                  round
                  type="warning"
                  >Check Validation and Send One-Time Code</el-button
                >
                <el-button
                  v-else
                  style="width: 350px"
                  round
                  type="primary"
                  @click="changeRegisterEmail"
                  >Change Email
                </el-button> </el-row
              ><el-divider>Enter the One-Time Code</el-divider
              ><el-row justify="center">
                <el-input
                  v-model="registerForm.forms.f2.otc"
                  :disabled="registerForm.forms.f2.otcVeri == ''"
                  style="width: 350px"
                  prefix-icon="el-icon-key"
              /></el-row>
            </el-form>
            <el-row justify="center" align="buttom">
              <el-divider></el-divider
              ><el-button-group>
                <el-button
                  @click="previousRegisterStep"
                  icon="el-icon-arrow-left"
                  round
                  type="primary"
                  plain
                  style="width: 80px" />
                <el-button
                  @click="checkOTC"
                  icon="el-icon-arrow-right"
                  round
                  type="primary"
                  style="width: 80px"
                  :disabled="
                    registerForm.forms.f2.otcVeri == ''
                  " /></el-button-group
            ></el-row>
          </div>
          <!--  -->
          <div v-if="registerStep == 2">
            <el-form
              ref="registerForm.forms.f3"
              :model="registerForm.forms.f3"
              :rules="rules3"
            >
              <el-divider>Set your password</el-divider
              ><el-row justify="center">
                <el-form-item prop="password">
                  <el-input
                    v-model="registerForm.forms.f3.password"
                    show-password
                    clearable
                    prefix-icon="el-icon-key"
                    style="width: 350px"
                  />
                </el-form-item>
                <br />
                <el-progress
                  :percentage="passwordIntensity"
                  :color="colors"
                  style="width: 350px"
                  :show-text="false"
              /></el-row>
              <el-divider>Confirm your password</el-divider
              ><el-row justify="center">
                <el-form-item prop="repassword">
                  <el-input
                    v-model="registerForm.forms.f3.repassword"
                    show-password
                    clearable
                    prefix-icon="el-icon-key"
                    style="width: 350px"
                    :disabled="passwordIntensity !== 100"
                  /> </el-form-item
              ></el-row>
            </el-form>
            <el-row justify="center" align="buttom">
              <el-divider></el-divider
              ><el-button-group>
                <el-button
                  @click="previousRegisterStep"
                  icon="el-icon-arrow-left"
                  round
                  type="primary"
                  plain
                  style="width: 80px" />
                <el-button
                  @click="register"
                  icon="el-icon-arrow-right"
                  round
                  type="primary"
                  style="width: 80px" /></el-button-group
            ></el-row>
          </div>
          <!--  -->
          <div v-if="registerStep == 3">
            <el-divider></el-divider>
            <el-row justify="center">
              <el-result
                icon="success"
                title="Finish!"
                sub-title="Congratulations! You can now use Rental Inspection System"
              >
              </el-result>
            </el-row>
            <el-row justify="center">
              <el-button
                type="primary"
                size="medium"
                @click="registerLogin"
                style="width: 200px"
                >Automatically Login</el-button
              ></el-row
            ><br /><el-row justify="center">
              <el-button
                type="primary"
                size="medium"
                @click="toHome"
                style="width: 200px"
                >Back to Home Page</el-button
              ></el-row
            >
          </div>
        </el-container></el-card
      ></el-row
    >
  </div>
</template>

<script>
import emailFormatCheck from "../utils/formValidator/emailFormatCheck.js";
import passwordIntensity from "../utils/formValidator/passwordIntensity";
import { APIurl } from "@/http";
import { ElMessage } from "element-plus";

export default {
  setup() {},
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
      colors: [
        { color: "#909399", percentage: 10 },
        { color: "#F56C6C", percentage: 30 },
        { color: "#E6A23C", percentage: 50 },
        { color: "#409EFF", percentage: 70 },
        { color: "#67C23A", percentage: 90 },
      ],
      rules1: {
        role: [
          { required: true, message: "Please select one.", trigger: "change" },
        ],
        name: [
          {
            required: true,
            message: "Please enter name.",
            trigger: "change",
          },
          {
            min: 8,
            message: "Too short.",
            trigger: "change",
          },
          {
            max: 18,
            message: "Too long.",
            trigger: "change",
          },
        ],
        mobile: [],
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
    submitRegisterSubform(formName) {
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
                  .post(APIurl + "/auth/Email_validation", form1)
                  .then((response) => {
                    if (response.status === 200) {
                      this.registerForm.forms.f2.otcVeri = response.data.v_code;
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
            // this.$root.currentUser.id = response.data.id;
            // this.$root.currentUser.avatar = response.data.avatar;
            // this.$root.currentUser.role = this.registerForm.forms.f1.role;
            // this.$root.currentUser.email = this.registerForm.forms.f2.email;
            // this.$root.loggedOn = true;
            localStorage.setItem("User", {
              id: response.data.id,
              role: this.loginForm.role,
            });
            localStorage.setItem("avatar", response.data.avatar);
            localStorage.setItem("Token", response.data.token);
            ElMessage({
              showClose: true,
              message: "Login successfully.",
              type: "success",
              center: true,
            });
            this.$router.push("/");
          }
        });
      // .catch((error) => {
      //   if (error.response.status === 400) {
      //     ElMessage({
      //       showClose: true,
      //       message: "Invalid email or password.",
      //       type: "error",
      //       center: true,
      //     });
      //   }
      // });
    },
  },
};
</script>