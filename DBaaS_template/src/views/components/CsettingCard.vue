<template>
  <div class="card">
    <div class="card-header pb-0 px-3">
      <div v-if="typeError" class="alert alert-danger alert-dismissible fade show custom-alert"><strong>Error!</strong>
        {{ typeError }}</div>
      <div v-if="providerError" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ providerError }}
      </div>
      <div v-if="errorNoSelectedProject" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ errorNoSelectedProject }}
      </div>
      <div v-if="computeOfferingError" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ computeOfferingError }}
      </div>
      <div v-if="storageOfferingError" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ storageOfferingError }}
      </div>
      <div v-if="errorClusterName" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ errorClusterName }}
      </div>
      <div v-if="errorClusterNameFormat" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ errorClusterNameFormat }}
      </div>
      <div v-if="errorPostgresPassword" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ errorPostgresPassword }}
      </div>
      <div v-if="passwordLengthError" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ passwordLengthError }}
      </div>
      <div v-if="errorDatabaseVersion" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ errorDatabaseVersion }}
      </div>
      <div v-if="errorClusterNameExists" class="alert alert-danger alert-dismissible fade show custom-alert">
        <strong>Error!</strong> {{ errorClusterNameExists }}
      </div>
      <h6 class="mb-0">Enter the Cluster Name and its Password</h6>
    </div>

    <div class="col-lg-8 col-md-12 col-12 w-50">
      <div class="">
        <div class="p-3 card-body">
          <div class="">
            <div class="">
              <label for="projectname" class="block  text-sm font-medium text-gray-900 dark:text-black">Cluster
                Name</label>
              <argon-input type="text" placeholder="Enter your Cluster Name" v-model="cluster_name" @change="updateName"
                @blur="checkClusterName" @input="validateClusterNameFormat" />


              <label for="projectname" class="block  text-sm font-medium text-gray-900 dark:text-black">Postgres
                Username
              </label>
              <argon-input type="text" placeholder="Enter your Postgres Username" valu='postgres' v-model="db_user"
                readonly />
              <label for="projectname" class="block  text-sm font-medium text-gray-900 dark:text-black">Postgres
                Password
              </label>
              <argon-input type="password" placeholder="Enter your Postgres Password" v-model="db_password"
                @change="updatePassword" @blur="validatePostgresPassword" />

              <h6 class="mb-3 text-sm">Database Version</h6>

              <select
                v-if="(providerName === 'OpenShift' || providerName === 'Kubernetes') && clusterType === 'Standalone'"
                :class="{ BGdark: isDarkMode }" class="form-select" aria-label="Default select example"
                @change="updateVersion" v-model="postgres_version" @blur="SelectPostgresVersion">
                <option value="16.3.0-debian-12-r12" selected>16</option>
                <option value="15.7.0-debian-12-r7">15</option>
                <option value="14.12.0-debian-12-r8">14</option>
              </select>

              <select
                v-else-if="(providerName === 'OpenShift' || providerName === 'Kubernetes') && clusterType === 'Multiple'"
                :class="{ BGdark: isDarkMode }" class="form-select" aria-label="Default select example"
                @change="updateVersion" v-model="postgres_version">
                <option value="16.3.0-debian-12-r8" selected>16</option>
                <option value="15.7.0-debian-12-r7">15</option>
              </select>

              <select v-else :class="{ BGdark: isDarkMode }" class="form-select" aria-label="Default select example"
                @change="updateVersion" v-model="postgres_version">
                <option value="16" selected>16</option>
                <option value="15">15</option>
                <option value="14">14</option>
                <option value="13">13</option>
                <option value="12">12</option>
              </select>


              <div v-if="providerName === 'CloudStack'">
                <h6 class="mb-3 mt-3 text-sm">Storage Provider</h6>
                <select :class="{ BGdark: isDarkMode }" class="form-select" aria-label="Default select example"
                  @click="updateMethod" v-model="backup_method">
                  <option value="nfs" selected>NFS</option>
                  <option value="s3">S3</option>
                </select>
              </div>


              <div v-if="providerName === 'CloudStack'" class="form-check form-switch mt-3 ">
                <input class="form-check-input" @click="toggleBackupSchedule()" type="checkbox">
                <label class=" text-sm mt-2" for="backupSwitch">Schedule Backup (Optional)</label>
              </div>

              <div v-if="isBackupScheduled">
                <div class="form-group mt-3 d-flex align-items-center">
                  <label class="text-sm col-md-3" for="retentionPeriod">Retention Period:</label>
                  <div class="input-group col-md-9">
                    <input type="email" class="form-control" id="retentionPeriod" v-model="retentionPeriod">
                    <select class="form-select bg-light" aria-label="Default select example" v-model="selected_value">
                      <option value="d" selected>days</option>
                      <option value="m">months</option>
                      <option value="y">years</option>
                    </select>
                  </div>
                </div>

                <div class="mx-3">
                  <h6>Scheduled Backup Settings</h6>

                  <div>
                    <label>
                      <input type="radio" v-model="backupType" value="daily" />
                      Daily Backups
                    </label>
                    <div v-if="backupType === 'daily'" class="form-group mt-3 d-flex align-items-center ">
                      <label class="text-sm col-md-3" for="">Backup Schedule:</label>
                      <div class="justify-content-end d-flex col-md-9">
                        <input type="email" class="form-control mx-2 col-md-3" value="Daily" readonly>
                        At<input type="number" class="form-control col-md-3 mx-2" v-model="selectedHour"> :
                        <input type="number" class="form-control col-md-3 ml-2" v-model="selectedMin">
                      </div>
                    </div>
                  </div>
                  <div>
                    <label>
                      <input type="radio" v-model="backupType" value="weekly" />
                      Weekly Backups
                    </label>
                    <div v-if="backupType === 'weekly'" class="form-group mt-3 d-flex align-items-center ">
                      <label class="text-sm col-md-3" for="">Backup Schedule:</label>
                      <div class="justify-content-end d-flex col-md-9">On
                        <select class="form-select col-md-3 mx-2" v-model="selectedDay">
                          <option v-for="day in days" :key="day" :value="day">
                            {{ day }}
                          </option>
                        </select>
                        At<input type="number" class="form-control col-md-3 mx-2" v-model="selectedHour"> :
                        <input type="number" class="form-control col-md-3 ml-2" v-model="selectedMin">
                      </div>
                    </div>

                  </div>
                  <div>
                    <label>
                      <input type="radio" v-model="backupType" value="monthly" />
                      Monthly Backups
                    </label>
                    <div v-if="backupType === 'monthly'" class="form-group mt-3 d-flex align-items-center ">
                      <label class="text-sm col-md-3" for="">Backup Schedule:</label>
                      <div class="justify-content-end d-flex col-md-9">On
                        <input type="number" class="form-control mx-2 col-md-3" v-model="selectedDate">
                        At<input type="number" class="form-control col-md-3 mx-2" v-model="selectedHour"> :
                        <input type="number" class="form-control col-md-3 ml-2" v-model="selectedMin">
                      </div>
                    </div>

                  </div>
                </div>
              </div>
              <div class="text-danger">
                {{ backupError }}
              </div>


              <br>


              <argon-button @click="createCluster" color="success" size="md" variant="gradient">
                Create Cluster
              </argon-button>


            </div>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
import axios from "axios";
import { mapState, mapActions } from "vuex";
import ArgonButton from "@/components/BB_Button.vue";
import { API_ENDPOINT } from "@/../apiconfig.js";
import ArgonInput from "@/components/BB_Input.vue";

export default {
  name: "billing-card",
  components: {
    ArgonButton,
    ArgonInput,

  },
  data() {
    return {
      apiUrl: API_ENDPOINT,

      selectedTools: [],
      postgres_version: "",
      cluster_name: "",
      user_id: "",
      provider_info: "",
      errorDatabaseVersion: "",
      errorClusterNameExists: "",
      errorNoSelectedProject: "",
      backendError: "",
      db_user: "postgres",
      db_password: "",
      backup_method: "",
      Username: "",
      nfsMountpoints: "",
      s3Mountpoints: "",
      backupError: "",
      mount_point: "",
      typeError: "",
      providerError: "",
      computeOfferingError: "",
      storageOfferingError: "",
      passwordLengthError: "",
      passwordLengthTimeout: null,
      updateName: '',
      errorClusterName: "",
      errorPostgresPassword: "",
      errorClusterNameFormat: "",
      isBackupScheduled: false,
      selectedHour: '12',
      selectedMin: "00",
      selectedDate: '10',
      selectedDay: 'Sunday',
      retentionPeriod: '',
      selected_value: '',
      date_time: '',
      backupType: '',
      days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      daysOfMonth: Array.from({ length: 31 }, (_, i) => i + 1),
      loading: false,

    };
  },

  methods: {
    ...mapActions(['updateSelectedVersion', 'updateClusterName', 'updateUsername', 'updatePassword', 'updateBackupMethod', 'updateRetention',
      'updateSelectedValue', 'updateMin', 'updateHour', 'updateDay', 'updateDate', 'updateBackupType'
    ]),
    updateVersion() {
      this.updateSelectedVersion(this.postgres_version);
      this.updateClusterName(this.cluster_name);
      this.updateUsername(this.db_user);
      this.updatePassword(this.db_password);
    },
    updateMethod() {
      this.updateBackupMethod(this.backup_method);
      this.listMountpoints();
    },

    toggleBackupSchedule() {
      this.isBackupScheduled = !this.isBackupScheduled;
    },

    listMountpoints() {

      // Retrieve the token from session storage

      const authToken = sessionStorage.getItem('token');

      if (!authToken) {

        console.error('Token not found in session storage');

        return;

      }

      const headers = {

        'Authorization': `Token ${authToken}`,

        'Content-Type': 'application/json'

      };

      axios.get(

        `${this.apiUrl}/api/v1/barman/list-mount-points?username=${this.Username}`, { headers },

      )

        .then((response) => {

          this.nfsMountpoints = response.data.nfs_mount_points;

          this.s3Mountpoints = response.data.s3_mount_points;

        })

        .catch((error) => {

          console.error('Error mounting s3:', error);

        })

    },

    validateClusterNameFormat() {
      const specialCharacterPattern = /^[!@#$%^&*()+=._-]/;
      const capitalLetterPattern = /^[A-Z]/;
      const numberPattern = /^[0-9]/;

      if (specialCharacterPattern.test(this.cluster_name) || capitalLetterPattern.test(this.cluster_name) || numberPattern.test(this.cluster_name)) {
        this.errorClusterNameFormat = "Cluster name cannot start with a number, special character, or capital letter.";
        setTimeout(() => {
          this.errorClusterNameFormat = "";
        }, 5000);
      } else {
        this.errorClusterNameFormat = "";
      }
    },


    checkClusterName() {
      // Reset errors
      this.errorClusterName = "";
      this.errorClusterNameExists = "";

      // Validate cluster name presence
      if (!this.cluster_name) {
        this.errorClusterName = "Cluster name is required.";
        setTimeout(() => {
          this.errorClusterName = "";
        }, 5000);
        return;
      }

      // Retrieve the token from session storage
      const authToken = sessionStorage.getItem('token');

      if (!authToken) {
        console.error('Token not found in session storage');
        return;
      }

      const headers = {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json'
      };

      // Check if cluster name already exists
      axios
        .get(
          `${this.apiUrl}/api/v1/cluster/check_cluster_exists/?cluster_name=${this.cluster_name}&project_id=${this.project_id}`,
          { headers }
        )
        .then((response) => {
          if (response.data.exists) {
            // Cluster name already exists
            this.errorClusterNameExists = "Cluster with the same name already exists";
            setTimeout(() => {
              this.errorClusterNameExists = "";
            }, 5000);
          }
        })
        .catch((error) => {
          console.log(error);
          // Handle errors from the cluster check API if needed
        });
    },

    validatePostgresPassword() {
      this.errorPostgresPassword = "";
      this.passwordLengthError = "";
      clearTimeout(this.passwordLengthTimeout);

      if (!this.db_password) {
        this.errorPostgresPassword = "Password is required.";
        this.passwordLengthTimeout = setTimeout(() => {
          this.errorPostgresPassword = "";
        }, 5000);
      } else if (this.db_password.length < 5 || this.db_password.length > 15) {
        this.passwordLengthError = "Password must be between 5 and 15 characters.";
        this.passwordLengthTimeout = setTimeout(() => {
          this.passwordLengthError = "";
        }, 5000);
      } else {
        this.errorPostgresPassword = "";
        this.passwordLengthError = "";
      }
    },

    createCluster() {
      this.updateRetention(this.retentionPeriod)
      this.updateSelectedValue(this.selected_value)
      this.updateMin(this.selectedMin)
      this.updateHour(this.selectedHour)
      this.updateDay(this.selectedDay)
      this.updateDate(this.selectedDate)
      this.updateBackupType(this.backupType)

      this.errorNoSelectedProject = "";
      this.backendError = "";

      if (!this.postgres_version) {
        this.errorDatabaseVersion = "Postgres version is required";
        setTimeout(() => {
          this.errorDatabaseVersion = "";
        }, 5000);
        return;
      }

      if (!this.project_id) {

        this.errorNoSelectedProject = "You have not selected any Project";
        setTimeout(() => {
          this.errorNoSelectedProject = "";
        }, 5000);
        return;
      }

      if (this.backup_method === "nfs") {
        this.mount_point = this.nfsMountpoints[0].mount_point;
        if (this.nfsMountpoints.length <= 0) {
          this.backupError = "NFS is not connected";
          return;
        } else {
          this.backupError = "";
        }

      } else if (this.backup_method === "s3") {


        this.mount_point = this.s3Mountpoints[0].mount_point;


        if (this.s3Mountpoints.length <= 0) {

          this.backupError = "S3 is not connected";

          return;

        } else {

          this.backupError = "";

        }

      } else {

        // If no storage provider is selected or no mount points available, set mount_point to blank

        this.mount_point = "";

      }


      if (!this.clusterType) {
        this.typeError = "Cluster type is required";
        setTimeout(() => {
          this.typeError = "";
        }, 5000);
        return;
      }
      if (!this.providerName) {
        this.providerError = "Provider is required";
        setTimeout(() => {
          this.providerError = "";
        }, 5000);
        return;
      }
      if (
        this.providerName !== "Kubernetes" &&
        this.providerName !== "OpenShift" &&
        this.providerName !== "Harvester" &&
        this.providerName !== "Nutanix" &&
        this.providerName !== "OpenStack" &&
        !this.computeOfferings
      ) {
        this.computeOfferingError = "Compute Offering is required";
        setTimeout(() => {
          this.computeOfferingError = "";
        }, 5000);
        return;
      }
      if (
        this.providerName !== "Kubernetes" &&
        this.providerName !== "OpenShift" &&
        this.providerName !== "Harvester" &&
        this.providerName !== "Nutanix" &&
        this.providerName !== "OpenStack" &&
        !this.selectedStorageOffering
      ) {
        this.storageOfferingError = "Storage Offering is required";
        setTimeout(() => {
          this.storageOfferingError = "";
        }, 5000);
        return;
      }

      // Retrieve the token from session storage
      const authToken = sessionStorage.getItem('token');

      if (!authToken) {
        console.error('Token not found in session storage');
        return;
      }

      const headers = {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json'
      };

      const fromData = {
        db_user: this.db_user,
        db_password: this.db_password,
        project: this.project_id,
        provider: this.providerName,
        cluster_type: this.clusterType,
        computeOffering: this.computeOfferings,
        storageOffering: this.selectedStorageOffering,
        storageClass: this.storageClass,
        size: this.size,
        cluster_name: this.cluster_name,
        postgres_version: this.postgres_version,
        backup_method: this.backup_method,
        mount_point: this.mount_point,
        flavor_id: this.flavors.flavor_id,
        k8sClass: this.k8sClass,
        osType: this.osType,
        airgap: this.airgap,
        // Conditionally add selectedK8sKeyName based on the provider
        ...(this.providerName === 'Kubernetes' && { selectedK8sKeyName: this.selectedK8sKeyName }),
      };
      console.log("form data print kro :", fromData);

      this.$router.push("/result");
      axios
        .post(`${this.apiUrl}/api/v1/cluster/`, fromData, { headers })
        .then(() => {
          this.scheduleBackup();
        })
        .catch((error) => {
          console.log(error.response.data.error);
          this.errorClusterNameExists = error.response.data.error;
          setTimeout(() => {
            this.errorClusterNameExists = "";
          }, 5000);


        });
    },

    scheduleBackup() {
      this.loading = true;
      if (this.backupType == 'weekly') {
        this.date_time = this.selectedDay
      } else if (this.backupType == 'monthly') {
        this.date_time = this.selectedDate
      } else {
        this.date_time = ''
      }
      const authToken = sessionStorage.getItem('token');

      // Check if the token exists
      if (!authToken) {
        console.error('Token not found in session storage');
        return;
      }

      // Set up the headers with the token
      const headers = {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json'
      };

      axios
        .post(
          `${this.apiUrl}/api/v1/barman/schedule-backup?server_name=${this.serverName}&retention=${this.retentionPeriod}${this.selected_value}&storage_method=${this.backup_method}&schedule_hour=${this.selectedHour}&schedule_minute=${this.selectedMin}${this.date_time !== '' ? '&schedule_day=' + this.date_time : ''}`, {}, { headers }
        )
        .then(() => {
          this.successMessage = "Backup scheduled successfully";
          setTimeout(() => {
            this.$router.push("/result");
          }, 5000);
        })
        .catch((error) => {
          this.errorMessage = error;
          setTimeout(() => {
            this.$router.push("/result");
          }, 5000);
        })
        .finally(() => {
          this.loading = false;
        });
    },


    fetchComputeOfferings() {
      const authToken = sessionStorage.getItem('token');

      if (!authToken) {
        console.error('Token not found in session storage');
        // Handle the absence of token as needed
        return;
      }

      const headers = {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json'
      };

      axios
        .get(`${this.apiUrl}/api/v1/compute_offerings/`, { headers })
        .then((response) => {
          this.computeOfferings = response.data;
        })
        .catch((error) => {
          console.error("Error fetching compute offerings:", error);
        });
    }

  },

  computed: {
    ...mapState([
      "clusterType",
      "dbPassword",
      "computeOfferings",
      "providerName",
      "project_name",
      "project_id",
      "selectedStorageOffering",
      "storageClass",
      "size",
      "flavors", "k8sClass",
      "osType",
      "airgap",
      "selectedK8sKeyName"

    ]),
    isDarkMode() {
      return this.$store.state.darkMode;
    },
  },
};
</script>

<style scoped>
.BGdark {
  background-color: #1d1e52;
  color: #fff;
}

.custom-alert {
  color: white;
  padding: 0.5rem;
  /* Reduce padding */

}
</style>
