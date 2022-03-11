<template>
  <div class="forgot-page">
    <el-row style="height: 100vh" justify="center" align="middle">
      <el-card shadow="hover" class="forgot-card"
        ><el-header>
          <el-row justify="center"
            ><el-link href="/" :underline="false">
              <img
                src="../assets/logo1.png"
                height="100"
                width="100" /></el-link
          ></el-row>
          <el-row
            justify="center"
            style="color: #365638; font-weight: bold; font-size: 20px"
          >
            FORGOT
          </el-row> </el-header
        ><el-row style="height: 60px"></el-row>
        <el-main
          ><div v-if="!otcChecked">
            <el-form
              ref="forgotVeriForm"
              :model="forgotForm"
              :rules="rules"
              size="medium"
            >
              <!-- Choose the role -->
              <el-form-item prop="role">
                <el-row justify="center">
                  <select-role
                    :role="forgotForm.role"
                    :roleBoxStyle="roleBoxStyle"
                    @changeRole="getRole"
                  />
                </el-row>
              </el-form-item>
              <el-form-item prop="email"
                ><el-row justify="center">
                  <el-popover
                    placement="bottom"
                    :show-arrow="false"
                    :width="220"
                    :offset="0"
                    :visible="
                      forgotForm.email !== '' && !/@/.test(forgotForm.email)
                    "
                    trigger="focus"
                  >
                    <template #reference>
                      <el-input
                        v-model="forgotForm.email"
                        clearable
                        placeholder="EMAIL"
                        class="login-input"
                        :disabled="forgotForm.otc != ''"
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
                        {{ forgotForm.email }}{{ suffix.value }}
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
                    v-if="forgotForm.otc == ''"
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
                        @click="changeForgotEmail"
                        >CHANGE EMAIL
                      </el-button></el-col
                    ><el-col :span="11">
                      <el-button
                        :disabled="forgotForm.otcCD != 0"
                        style="
                          width: 100%;
                          color: #ffffff;
                          font-weight: bold;
                          background-color: #365638;
                        "
                        @click="emailVerification"
                        >RESEND<span v-if="forgotForm.otcCD != 0"
                          >({{ forgotForm.otcCD }}s)</span
                        >
                      </el-button></el-col
                    ></el-row
                  >
                </el-row></el-form-item
              ></el-form
            >
            <!-- otc input --><el-form
              ref="forgotOtcForm"
              :model="forgotForm"
              :rules="rules"
              size="medium"
            >
              <el-form-item prop="otcCheck">
                <el-row justify="center">
                  <el-input
                    v-model="forgotForm.otcCheck"
                    placeholder="ENTER ONE-TIME CODE"
                    :disabled="forgotForm.otc == ''"
                    class="login-input"
                    ><template #prefix
                      ><i
                        class="el-input__icon el-icon-key"
                        style="color: #365638; font-weight: bold"
                      ></i></template></el-input></el-row
              ></el-form-item>
              <el-button
                style="
                  width: 100%;
                  color: #ffffff;
                  font-weight: bold;
                  background-color: #365638;
                "
                @click="checkOTC"
                :disabled="forgotForm.otcCheck === ''"
                >VERIFICATE
              </el-button>
            </el-form>
          </div>
          <div v-else>
            <el-row style="height: 30px"></el-row>
            <el-row
              justify="center"
              style="color: #365638; font-weight: bold; font-size: 15px"
            >
              SUCCESSFULLY VERIFICATE EMAIL
            </el-row>
            <el-row
              justify="center"
              style="color: #365638; font-weight: bold; font-size: 15px"
            >
              PLEASE RESET YOUR PASSWORD </el-row
            ><el-row style="height: 30px"></el-row>
            <el-form
              ref="forgotPasswordForm"
              :model="forgotForm"
              :rules="rules"
              size="medium"
            >
              <el-form-item prop="password"
                ><el-row justify="center">
                  <el-popover :show-arrow="false" :width="240" :offset="20">
                    <template #reference>
                      <el-input
                        v-model="forgotForm.password"
                        show-password
                        clearable
                        class="login-input"
                        placeholder="PASSWORD"
                        :disabled="forgotForm.otc === ''"
                      >
                        <template #prefix
                          ><i
                            class="el-input__icon el-icon-key"
                            style="color: #365638; font-weight: bold"
                          ></i
                        ></template> </el-input></template
                    ><password-tip
                      :password="forgotForm.password"
                      :passwordIntensity="passwordIntensity"
                      :textColor="'#365638'"
                    />
                  </el-popover> </el-row
              ></el-form-item>
              <el-form-item prop="repassword"
                ><el-row justify="center">
                  <el-input
                    v-model="forgotForm.repassword"
                    show-password
                    clearable
                    class="login-input"
                    placeholder="COMFIRM PASSWORD"
                    :disabled="passwordIntensity !== 100"
                    ><template #prefix
                      ><i
                        class="el-input__icon el-icon-key"
                        style="color: #365638; font-weight: bold"
                      ></i
                    ></template> </el-input></el-row></el-form-item
              ><!-- send otc button--><el-form-item>
                <el-row justify="center">
                  <el-button
                    style="
                      width: 100%;
                      color: #ffffff;
                      font-weight: bold;
                      background-color: #365638;
                    "
                    @click="submitForgot"
                  >
                    SUBMIT
                  </el-button></el-row
                >
              </el-form-item>
            </el-form>
          </div></el-main
        ></el-card
      >
    </el-row>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
import { APIurl } from "@/http";
import { reactive, ref } from "vue";
import { emailSuffix } from "../utils/formValidator/emailFormatCheck";
import passwordIntensity from "../utils/formValidator/passwordIntensity";
import SelectRole from "../components/auth/selectRole.vue";
import PasswordTip from "../components/auth/passwordTip.vue";

export default {
  components: { SelectRole, PasswordTip },

  data() {
    const checkPassword = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please confirm the password."));
      } else if (value !== this.forgotForm.password) {
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
      currentRow: null,
      forgotForm: reactive({
        id: "",
        email: "",
        password: "",
        repassword: "",
        otc: "",
        otcCheck: "",
        otcCD: 0,
        otcExpire: 0,
        role: "",
      }),
      rules: {
        role: [
          {
            required: true,
            message: "Please select your role.",
            trigger: "blur",
          },
        ],
        email: [
          {
            required: true,
            message: "Please enter your email.",
            trigger: "change",
          },
          {
            // validator: emailFormatCheck,
            type: "email",
            message: "Invalid email format.",
            trigger: "change",
          },
        ],
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
        otcCheck: [
          {
            required: true,
            message: "Please enter One-Time Code.",
            trigger: "blur",
          },
        ],
      },
      otcChecked: ref(false),
      Clicked: ref(false),
      passwordIntensity: 0,
    };
  },
  methods: {
    getRole(role) {
      this.forgotForm.role = role;
    },
    completeEmail(row) {
      this.forgotForm.email += row;
    },
    changeForgotEmail() {
      this.forgotForm.otc = "";
      this.forgotForm.otcCheck = "";
      this.forgotForm.otcExpire = 0;
    },
    resendEmailTimer() {
      this.forgotForm.otcCD = 10;
      var timer = setInterval(() => {
        if (this.forgotForm.otcCD > 0) {
          this.forgotForm.otcCD -= 1;
        } else {
          clearInterval(timer);
        }
      }, 1000);
    },
    emailVerification() {
      this.Clicked = true;
      this.$refs["forgotVeriForm"].validate((valid) => {
        if (valid) {
          let form1 = {
            role: this.forgotForm.role,
            email: this.forgotForm.email,
          };
          this.$axios
            .post(APIurl + "/auth/emailValid", form1)
            .then((response) => {
              if (response.status === 200) {
                this.forgotForm.email = "";
                this.forgotForm.role = "";
                ElMessage({
                  showClose: true,
                  message: `${form1.email} has not been registered as a ${form1.role}.`,
                  type: "error",
                  center: true,
                });
              }
            })
            .catch((error) => {
              if (error.response.status === 400) {
                this.forgotForm.id = error.response.data.id;
                this.$axios
                  .post(APIurl + "/email/Validation", {
                    email: this.forgotForm.email,
                    require_type: "r",
                  })
                  .then((response) => {
                    if (response.status === 200) {
                      this.forgotForm.otc = response.data.v_code;
                      let time = new Date();
                      this.forgotForm.otcExpire =
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
            });
        } else {
          return false;
        }
      });
    },
    checkOTC() {
      let time = new Date();
      if (
        this.forgotForm.otcExpire > 0 &&
        time.getTime() > this.forgotForm.otcExpire
      ) {
        ElMessage({
          showClose: true,
          message: "One-Time Code is expired.",
          type: "error",
          center: true,
        });
      } else {
        if (this.forgotForm.otc === this.forgotForm.otcCheck) {
          this.otcChecked = true;
        } else {
          (this.forgotForm.otcCheck = ""),
            ElMessage({
              showClose: true,
              message: "One-Time Code is incorrect.",
              type: "error",
              center: true,
            });
        }
      }
    },
    submitForgot() {
      this.$refs["forgotPasswordForm"].validate((valid) => {
        if (valid) {
          this.$axios
            .patch(APIurl + "/auth/user_password/" + this.forgotForm.id, {
              user_role: this.forgotForm.role,
              mode: "reset",
              new_password: this.forgotForm.password,
              old_password: "",
            })
            .then((response) => {
              if (response.status === 200) {
                this.$router.push("/");
                ElMessage({
                  showClose: true,
                  message: "Successfully reset password.",
                  type: "success",
                  center: true,
                });
              }
            });
        } else {
          return false;
        }
      });
    },
  },
  computed: {
    managerStyle() {
      return this.forgotForm.role === "manager" ? "#ffffff" : "#788f77";
    },
    tenantStyle() {
      return this.forgotForm.role === "tenant" ? "#ffffff" : "#788f77";
    },
    roleBoxStyle() {
      return this.Clicked && this.forgotForm.role === ""
        ? "#f56c6c"
        : "#365638";
    },
  },
};
</script>

<style scoped>
.forgot-card {
  width: 360px;
  height: 510px;
  filter: saturate(80%);
  border: solid #365638;
  background-color: rgba(255, 255, 255, 0.9);
}

.login-input :deep(input) {
  color: #365638;
  font-weight: bold;
  border: solid #365638;
  height: 40px;
}

.login-input :deep(input::-webkit-input-placeholder) {
  color: #788f77;
}

.forgot-page {
  background-image: url("../assets/loginbg1.jpg");
  background-size: cover;
  background-position: center;
}
</style>