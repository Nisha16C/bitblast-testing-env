<template>
  <main>
    <div class="container-fluid py-8">
      <div class="page-header min-height-100" style="
            margin-right: -24px;
            margin-left: -54%;
          ">
      </div>
      <div class="card shadow-lg mt-n6  w-full">
        <div class="card-body p-0">
           <!-- Overlay Text "Activity Logs" -->
           <div class="overlay-text bg-white text-center p-3" :class="{ 'dark-overlay': isDarkMode }">
            <h2 class="mb-0">Monitoring</h2>
          </div>
          <div class="row gx-4">
            <iframe class="min-vh-100" width="100%" height="100%" :src="embedUrl" frameborder="0"
              allowfullscreen></iframe>
          </div>
        </div>
      </div>
    </div>

  </main>
</template>

<script>
import setNavPills from "@/assets/js/nav-pills.js";
import setTooltip from "@/assets/js/tooltip.js";

export default {
  name: "profile",
  data() {
    return {
      user_id: '',
      embedUrl: {
        light: 'http://172.16.1.186:3000/d/07/postgresql-for-admins?orgId=1&refresh=10s&theme=light',
        dark: 'http://172.16.1.186:3000/d/07/postgresql-for-admins?orgId=1&refresh=10s&theme=dark'
      },
    };
  },
  created() {
    this.username = sessionStorage.getItem('username');
    this.user_id = sessionStorage.getItem('user_id');
    this.setEmbedUrl();
  },
  methods: {
    setEmbedUrl() {
      // Check if the user is an admin
      if (this.username === 'admin') {
        // Select the appropriate URL based on dark mode
        this.embedUrl = this.isDarkMode ? this.embedUrl.dark : this.embedUrl.light;
      } else {
        // If the user is not an admin, use the URL for other users
        // http://172.16.1.54:3000/d/08/postgresql-for-other-users?orgId=1&refresh=10s&editIndex=2&var-DS_PROMETHEUS=bc775041-25c7-4cee-9226-c4278a324020&var-interval=%24__auto_interval_interval&var-user=${this.username}&var-datname=All&var-mode=All&from=1713794948248&to=1713795248249&theme=light
        this.embedUrl = `http://172.16.1.186:3000/d/07/postgresql-for-admins?orgId=1&refresh=10s&theme=light
  ` ;
      }
    }
  },
  mounted() {
    this.$store.state.isAbsolute = true;
    setNavPills();
    setTooltip();
  },
  beforeMount() {
    this.$store.state.imageLayout = "profile-overview";
    this.$store.state.showNavbar = true;
    this.$store.state.showFooter = true;
    this.$store.state.hideConfigButton = true;
    document.body.classList.add("profile-overview");
  },
  beforeUnmount() {
    this.$store.state.isAbsolute = false;
    this.$store.state.imageLayout = "default";
    this.$store.state.showNavbar = true;
    this.$store.state.showFooter = true;
    this.$store.state.hideConfigButton = false;
    document.body.classList.remove("profile-overview");
  },
  computed: {
    isDarkMode() {
      return this.$store.state.darkMode;
    },
  }
};
</script>

<style scoped>
.overlay-text {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  text-align: center;
  background-color: white;
  z-index: 2;
}

.dark-overlay {
  position: absolute;
  top: 0%;
  left: 0%;
  width: 99.5%;
  height: 9.5%;
  text-align: center;
  color: white;
  background-color: rgb(15, 15, 15);
  padding: 10px;
  border-radius: 8px;
  z-index: 2;
}
</style>