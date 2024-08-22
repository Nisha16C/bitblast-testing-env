<template>
  <div class="card">
    <div class="card-header pb-0">
      <h6 class="text-2xl"> Database Info </h6>
    </div>
    <div v-if="loading" class="text-center mt-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="card-body px-0 pt-0 pb-2">
      <div v-if="localClusters.length === 0" class="text-center">No Cluster found in the Selected Project</div>
      <div v-else class="table-responsive p-0">
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-md font-weight-bolder opacity-7"> Database ID & Name </th>
              <th class="text-uppercase text-secondary text-md font-weight-bolder opacity-7 ps-2">Database Type &
                Version</th>
              <th class="text-uppercase text-secondary text-md font-weight-bolder opacity-7 ps-2">Storage Provider</th>

              <th class="text-center text-uppercase text-secondary text-md font-weight-bolder opacity-7"> Provider Name
              </th>
              <th class="text-center text-uppercase text-secondary text-md font-weight-bolder opacity-7"> Created On
              </th>
              <th class="text-center text-uppercase text-secondary text-md font-weight-bolder opacity-7"> Updated On
              </th>
              <th class="text-secondary opacity-7"></th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(cluster, index) in localClusters" :key="index">
              <td class="no-border">
                <div class="d-flex px-2 py-1">
                  <div>
                    <img
                      :src="cluster.cluster_type === 'Multiple' ? require('@/assets/img/ha.webp') : (this.$store.state.darkMode || this.$store.state.sidebarType === 'bg-default' ? logoWhite : logo)"
                      class="avatar avatar-sm me-3" alt="clusterImage" />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-md">{{ cluster.id }}</h6>
                    <p class="text-md text-secondary mb-0">{{ cluster.cluster_name }}</p>
                  </div>
                </div>
              </td>

              <td>
                <p class="text-md font-weight-bold mb-0">{{ cluster.cluster_type }}</p>
                <p class="text-md text-secondary mb-0">{{ cluster.database_version }}</p>
                <!-- <p class="text-md text-secondary mb-0">{{ cluster.backup_method }}</p> -->
              </td>
              <td class="align-middle text-center text-md">
                <span class="text-secondary text-md font-weight-bold">{{ cluster.backup_method }}</span>
              </td>
              <td class="align-middle text-center text-md">
                <!-- Assuming 'provider' is a property in your cluster data -->
                <span class="text-secondary text-md font-weight-bold">{{ cluster.provider }}</span>
              </td>

              <td class="align-middle text-center">
                <span class="text-secondary text-md font-weight-bold">{{ formatDate(cluster.created_date) }}</span>
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-md font-weight-bold">{{ formatDate(cluster.updated_date) }}</span>
              </td>


              <td class="align-middle">

                <argon-button color="success" size="md" variant="gradient" @click="viewCluster(cluster.cluster_name)"
                  type="button" class="btn btn-danger" data-toggle="modal" data-target="#viewModal">
                  View
                </argon-button>
                <argon-button color="danger" size="md" variant="gradient"
                  @click="prepareDelete(cluster.cluster_name, cluster.provider)" type="button"
                  class="ml-4 btn btn-danger" data-toggle="modal" data-target="#exampleModal">
                  Delete
                </argon-button>
              </td>

              <!-- New TD with SVG if provider is 'Kubernetes' -->
              <td v-if="cluster.provider === 'Kubernetes'" class="align-middle text-center text-md">
                <svg @click="openModal(cluster.cluster_name, cluster.k8s_key_name)" xmlns="http://www.w3.org/2000/svg"
                  width="26" height="26" fill="currentColor" class="bi bi-terminal cursor blink-on-hover"
                  viewBox="0 0 16 16" id="IconChangeColor">
                  <path
                    d="M6 9a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3A.5.5 0 0 1 6 9zM3.854 4.146a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2z"
                    id="mainIconPathAttribute"></path>
                  <path
                    d="M2 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h12z"
                    id="mainIconPathAttribute"></path>
                </svg>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div class="pagination-container">
          <button @click="fetchPage(page - 1)" :disabled="page === 1" class="pagination-button">Previous</button>
          <span class="pagination-info">Page {{ page }} of {{ totalPages }}</span>
          <button @click="fetchPage(page + 1)" :disabled="page === totalPages" class="pagination-button">Next</button>
        </div>

      </div>
    </div>
  </div>
  <!-- Modal -->
  <div v-if="showModal" class="terminal2" @click="closeModal">
    <div class="terminal1" @click.stop>

      <Terminal v-if="showTerminal" :cluster_name="selectedClusterName" :k8s_key_name="selectedKeyName"
        @click="showTerminal = true" />
      <button @click="closeModal" class="btn btn-secondary close-terminal-btn">Close Terminal</button>

    </div>
  </div>
  <!-- modal of cluster detail -->
  <div class="modal fade" id="viewModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">

    <div class="modal-dialog custom-modal-dialog" role="document">

      <div class="modal-content custom-modal-content" :class="{ 'dark-mode': isDarkMode }">

        <div class="modal-header">

          <!-- <h5 class="modal-title" id="exampleModalLabel">Cluster Details</h5> -->

          <argon-button color="white" size="md" variant="outline" @click="openDetails" type="button"
            class="ml-4 mt-2 text-dark ">

            <h5>Cluster Details</h5>

          </argon-button>

          <argon-button v-if="currentClusterType === 'Multiple'" color="white" size="md" variant="outline"
            @click="openArtifacts" type="button" class="ml-4 mt-2 text-dark ">

            <h5>Cluster Member</h5>

          </argon-button>

          <button type="button" class="close" data-dismiss="modal" aria-label="Close">

            <span aria-hidden="true">&times;</span>

          </button>

        </div>

        <div class="modal-body">

          <h3>{{ clusterName }}</h3>

          <div v-if="artifacts">

            <artifacts />

          </div>

          <div v-else>

            <p v-if="contentList.length > 0" v-html="addLineBreaks(contentList[0].content)"></p>

          </div>

        </div>

        <div class="modal-footer">

          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

        </div>

      </div>

    </div>

  </div>

  <!-- Delete Modal -->
  <div v-show="deleteModal" class="modal fade" id="exampleModal" tabindex="-1" role="dialog"
    aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content" :class="{ 'dark-mode': isDarkMode }">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Delete Cluster</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          Are You Sure Want to delete cluster "{{ deleteClusterName }}" ?
          <argon-input type="text" placeholder="Enter Cluster Name" v-model="confirmDlt" />
        </div>


        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button @click="deleteCluster()" :disabled="!confirm" type="button" data-dismiss="modal"
            class="btn btn-danger"> Delete</button>
        </div>
      </div>
    </div>
  </div>
  <AuthorTable :selectedProject="projectName" />


</template>

<script>
import axios from "axios";
import ArgonButton from "@/components/BB_Button.vue";
import ArgonInput from "@/components/BB_Input.vue";

import { API_ENDPOINT } from '@/../apiconfig.js';
import logo from "@/assets/img/db-png.png";
import logoWhite from "@/assets/img/logo3.png";
import Terminal from './terminal.vue';
import artifacts from "../components/artifacts.vue";


export default {
  name: "UserCluster-table",
  components: {
    ArgonInput,
    ArgonButton,
    Terminal,
    artifacts
  },
  data() {
    return {
      artifacts: false,
      currentClusterType: '',
      apiUrl: API_ENDPOINT,
      contentList: [],
      deleteClusterName: '',
      selectedProvider: '',
      provider_info: '',
      loading: true,
      logo,
      logoWhite,
      confirmDlt: '',
      localClusters: [], // Array to hold fetched clusters
      page: 1, // Current page of pagination
      pageSize: 5, // Number of clusters per page
      totalPages: 1, // Total number of pages
      clusterName: '',
      deleteModal: false, // Add this line
      showModal: false,
      k8sKeyName: '',
      showTerminal: false,
      selectedClusterName: '',
      selectedKeyName: ''

    }
  },
  props: {
    clusters: {
      type: Array,
      required: true,
    },
  },

  computed: {
    isDarkMode() {
      return this.$store.state.darkMode;
    },
    confirm() {
      if (this.deleteClusterName === this.confirmDlt) {
        return true
      }
      else {
        return false
      }
    }
  },

  watch: {
    clusters: {
      immediate: true,
      handler(newVal) {
        this.localClusters = newVal;
      },
    },
  },

  created() {
    this.Username = sessionStorage.getItem('username');
    this.user_id = sessionStorage.getItem('user_id');
    this.fetchPage(this.page);
  },
  methods: {
    openModal(cluster_name, k8s_key_name) {
      this.showModal = true;
      this.selectedClusterName = cluster_name;
      this.selectedKeyName = k8s_key_name;
      this.showTerminal = true;

    },
    closeModal() {
      this.showModal = false;
    },
    openDetails() {
      this.artifacts = false;
    },

    openArtifacts() {
      this.artifacts = true;
    },
    fetchPage(page) {
      if (page < 1 || page > this.totalPages) return;

      this.loading = true;
      this.page = page;
      const authToken = sessionStorage.getItem('token');

      if (!authToken) {
        console.error('Token not found in session storage');
        this.loading = false;
        return;
      }

      const headers = {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json'
      };

      axios.get(`${this.apiUrl}/api/v1/clusters/userlist/`, {
        headers,
        params: {
          page: this.page,
          page_size: this.pageSize
        }
      })
        .then(response => {
          this.localClusters = response.data.results;
          this.totalPages = Math.ceil(response.data.count / this.pageSize);
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching clusters:', error);
          this.loading = false;
        });
    },

    prepareDelete(clusterName, provider_name) {
      this.deleteClusterName = clusterName;
      this.selectedProvider = provider_name
    },
    deleteCluster() {

      // Retrieve the token from sessionStorage
      const authToken = sessionStorage.getItem('token');

      if (!authToken) {
        console.error('Token not found in session storage');
        return;
      }

      const headers = {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json'
      };

      axios
        .get(`${this.apiUrl}/api/v1/providers/by-username-and-name/${this.selectedProvider}/`, { headers })
        .then((response) => {
          this.provider_info = response.data;

          const formData = {
            cluster_name: this.deleteClusterName,
            provider_name: this.selectedProvider,
            provider_endpoint: this.provider_info.provider_url,
            provider_access_token: this.provider_info.access_token,
            provider_secret_key: this.provider_info.secret_key,
            kubeconfig_data: this.provider_info.kubeconfig_data,
          };

          this.$router.push('/delete');

          axios.post(`${this.apiUrl}/api/v1/delete-cluster/`, formData, { headers })
            .then(() => {
              this.fetchclusters_list();
            })
            .catch(error => {
              console.error('Error deleting cluster:', error);
              // Handle error, show a message, etc.
              this.toggleModal1();
            });
        })
        .catch(error => {
          console.error('Error fetching provider info:', error);
        });
    },

    viewCluster(clusterName) {
      this.clusterName = clusterName;

      const cluster = this.localClusters.find(c => c.cluster_name === clusterName);

      this.currentClusterType = cluster ? cluster.cluster_type : '';


      // Get the token from sessionStorage
      const authToken = sessionStorage.getItem('token');

      if (!authToken) {
        console.error('Token not found in session storage');
        return;
      }

      // Set up the headers with the token
      const headers = {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json'
      };

      axios.get(`${this.apiUrl}/api/v1/result/content/${clusterName}/`, { headers })
        .then(response => {
          this.contentList = response.data;
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },

    addLineBreaks(text) {
      const formattedContent = text.replace(/([^:\n]+):/g, '<h class="text-md text-purple-600">$1</h>:');
      return formattedContent.replace(/\n/g, '<br>');
    },

    async fetchclusters_list() {
      try {
        const token = sessionStorage.getItem('token'); // Retrieve the token from session storage

        if (!token) {
          throw new Error('Token not found in session storage');
        }

        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        // Make a GET request to the endpoint with headers
        const response = await axios.get(`${this.apiUrl}/api/v1/cluster/`, { headers });

        // Update the clusters_list data with the fetched data
        this.clusters_list = response.data.reverse();
        this.loading = false;
      } catch (error) {
        console.error('Error fetching clusters_list:', error);
        this.loading = false;
      }
      this.fetchPage(this.page);
    },

    toggleModal1: function () {
      this.showModal = !this.showModal;
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('en-US', options);
    },
  }
};
</script>

<style scoped>
.no-border {
  border: none !important;
}

/* Modal styles */

.terminal2 {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.terminal1 {
  width: 900px;
  height: 650px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  position: relative;
  z-index: 1001;
}

.close-terminal-btn {
  position: absolute;
  /* top: 200px; */
  bottom: -2px;
  right: 10px;
  background-color: #f44336;
  /* Red color */
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.close-terminal-btn:hover {
  background-color: #d32f2f;
  /* Darker red */
}

.cursor {
  cursor: pointer;
  /* Changes the cursor to a pointer when hovering over the SVG */
  vertical-align: middle;
  /* Align SVG icon in the middle of the cell */

}

.blink-on-hover {
  transition: fill 0.2s ease-in-out;
}

.blink-on-hover:hover {
  fill: rgb(0, 255, 157);
  animation: blink-animation 1s infinite;
}

@keyframes blink-animation {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.5;
  }
}

.dark-mode {
  background-color: #1d1e52;
  color: #ffffff;
}

.card-body {
  position: relative;
}

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  margin-left: 0px;
  /* Move the pagination container to the left */
}

.pagination-button {
  background-color: #3ba73e;
  border: none;
  color: white;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin-right: 10px;
  cursor: pointer;
  border-radius: 4px;
}

.pagination-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.pagination-info {
  margin: 0 10px;
  font-size: 14px;
}

.custom-modal-dialog {

  max-width: 50%;
  /* Adjust the width as needed */

}

.custom-modal-content {

  height: 60vh;
  /* Adjust the height as needed */

  overflow: auto;
  /* Allows scrolling if content overflows */

}
</style>
