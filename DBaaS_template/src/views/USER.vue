<template>
    <main>
        <div class="container-fluid mt-7">
            <div class="card shadow-lg mt-n6">
                <div class="card-body p-3">
                    <div class="row gx-4">
                        <router-link to="/User-Management">
                            <i class="fas fa-arrow-left mr-2"></i>
                        </router-link><br>
                        <div class="col-auto">
                            <div class="avatar avatar-xl position-relative">
                                <img src="../assets/img/team-6.jpg" alt="profile_image"
                                    class="shadow-sm w-100 border-radius-lg" />
                            </div>
                        </div>
                        <div class="col-auto my-auto">
                            <div class="h-100">
                                <h5 class="mb-1">New User Create</h5>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="py-4 container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-body">
                            <p class="text-uppercase text-sm">User Information</p>
                            <div class="row">
                                <div class="col-md-6">
                                    <label for="first_name" class="form-control-label">First Name</label>
                                    <argon-input v-model="userData.first_name" type="text" placeholder="First Name" />
                                    <div class="text-danger">{{ errors.first_name }}</div>
                                </div>
                                <div class="col-md-6">
                                    <label for="last_name" class="form-control-label">Last Name</label>
                                    <argon-input v-model="userData.last_name" type="text" placeholder="Last Name" />
                                    <div class="text-danger">{{ errors.last_name }}</div>
                                </div>
                                <div class="col-md-6">
                                    <label for="username" class="form-control-label">Username</label>
                                    <argon-input v-model="userData.username" type="text" placeholder="Username" />
                                    <div class="text-danger">{{ errors.username }}</div>
                                </div>
                                <div class="col-md-6">
                                    <label for="email" class="form-control-label">Email Address</label>
                                    <argon-input v-model="userData.email" type="email" placeholder="user@example.com"
                                        @input="validateEmail" />
                                    <div class="text-danger">{{ errors.email }}</div>
                                    <div v-if="emailValidationMessage" class="text-info">{{ emailValidationMessage }}
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <label for="password" class="form-control-label">Password</label>
                                    <argon-input v-model="userData.password" type="password"
                                        placeholder=". . . . . . . ." />
                                    <div class="text-danger">{{ errors.password }}</div>

                                </div>
                                <div class="col-md-6">
                                    <label for="cpassword" class="form-control-label">Confirm Password</label>
                                    <argon-input v-model="userData.cpassword" type="password"
                                        placeholder=". . . . . . . ." />
                                    <div class="text-danger">{{ errors.cpassword }}</div>
                                </div>
                                <div class="ml-2">
                                    <h6>Assign Role</h6>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" id="adminRole" value="Admin"
                                            v-model="userData.role">
                                        <label class="form-check-label" for="adminRole">Admin</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" id="standardRole" value="Standard"
                                            v-model="userData.role">
                                        <label class="form-check-label" for="standardRole">Standard</label>
                                    </div>
                                </div>

                                <div class="my-3 ml-2 ">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" v-model="agreeTerms" value=""
                                            id="flexCheckDefault">
                                        <label class="form-check-label" for="flexCheckDefault">
                                            I agree with the <a href="#">terms and conditions</a>.
                                        </label>
                                        <!-- <div class="text-danger">{{ errors.email }}</div> -->
                                    </div>
                                </div>

                                <div class="">
                                    <argon-button color="success" size="md" variant="gradient" @click="CreateUser()"
                                        type="button" class="ml-4 btn btn-danger" data-toggle="modal"
                                        data-target="#exampleModal" :disabled="!agreeTerms">Create New
                                        User</argon-button>
                                    <div class="text-success">{{ successMessage }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>
</template>

<script>
import setNavPills from "@/assets/js/nav-pills.js";
import setTooltip from "@/assets/js/tooltip.js";
// import ProfileCard from "./components/ProfileCard.vue";
import ArgonInput from "@/components/BB_Input.vue";
import argonButton from "@/components/BB_Button.vue";
import { API_ENDPOINT } from '@/../apiconfig.js';

import axios from 'axios';

const body = document.getElementsByTagName("body")[0];

export default {
    name: "USER",
    data() {
        return {
            apiUrl: API_ENDPOINT,
            showMenu: false,
            userData: {
                first_name: '',
                username: '',
                email: '',
                phone: '',
                password: '',
                cpassword: '',
                role: '' // Add a field for the selected role

            },
            errors: {
                first_name: '',
                username: '',
                email: '',
                phone: '',
                password: '',
                cpassword: '',
                role: '' // Add a field for the selected role

            },
            successMessage: '',
            agreeTerms: false,
            emailValidationMessage: ''

        };
    },
    components: { ArgonInput, argonButton },
    methods: {
        validatePassword() {
            this.passwordLengthError = "";
            clearTimeout(this.passwordLengthError);

            if (this.db_password.length < 5 || this.db_password.length > 15) {
                this.passwordLengthError =
                    "Password must be between 5 and 10 characters";
                this.passwordLengthTimeout = setTimeout(() => {
                    this.passwordLengthError = "";
                }, 5000);
            }
        },
        validateEmail() {
            const email = this.userData.email;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email)) {
                this.errors.email = 'Invalid email format';
            } else {
                this.errors.email = ''; // Clear error message if email format is valid
            }
        },
        CreateUser() {
            this.clearErrors();
            // Validate required fields
            const requiredFields = ['first_name', 'username', 'email', 'password', 'cpassword'];
            let hasErrors = false;

            requiredFields.forEach(field => {
                if (!this.userData[field]) {
                    this.errors[field] = 'This field is required';
                    hasErrors = true;
                }
            });

            // Validate password and confirm password match
            if (this.userData.password !== this.userData.cpassword) {
                this.errors.cpassword = 'Password do not match';
                hasErrors = true;
            }

            if (hasErrors) {
                return; // Stop execution if there are errors
            }

            // Retrieve the authentication token from sessionStorage
            const authToken = sessionStorage.getItem('token');

            // Prepare headers with the authentication token
            const headers = {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            };

            // Make a POST request to register a new user with headers
            axios.post(`${this.apiUrl}/api/v1/register/`, this.userData, { headers })
                .then(() => {
                    this.successMessage = `Well done! ${this.userData.username} user is successfully created.`;
                    this.clearForm();
                    this.agreeTerms = false;
                    // Delayed removal of success message after 5 seconds
                    setTimeout(() => {
                        this.successMessage = '';
                    }, 5000);
                })
                .catch(error => {
                    // Handle errors
                    console.error('Error creating user:', error);
                    if (error.response) {
                        // The request was made and the server responded with a status code
                        console.error('Response data:', error.response.data);
                        console.error('Response status:', error.response.status);

                        // Check for specific error message from the backend
                        if (error.response.data.username) {
                            this.errors.username = 'This username is already exists.';
                            setTimeout(() => {
                                this.errors.username = ''; // Clear error message after 5 seconds
                            }, 5000);
                        }
                    } else if (error.request) {
                        // The request was made but no response was received
                        console.error('No response received:', error.request);
                    } else {
                        // Something else happened while setting up the request
                        console.error('Error setting up request:', error.message);
                    }
                });
        },

        clearErrors() {
            // Clear all error messages
            for (const field in this.errors) {
                this.errors[field] = '';
            }
        },
        clearForm() {
            // Clear all input fields
            for (const field in this.userData) {
                this.userData[field] = '';
            }

        },

        mounted() {
            this.$store.state.isAbsolute = true;
            setNavPills();
            setTooltip();
        },
        beforeMount() {
            this.$store.state.imageLayout = "profile-overview";
            this.$store.state.showNavbar = false;
            this.$store.state.showFooter = true;
            this.$store.state.hideConfigButton = true;
            body.classList.add("profile-overview");
        },
        beforeUnmount() {
            this.$store.state.isAbsolute = false;
            this.$store.state.imageLayout = "default";
            this.$store.state.showNavbar = true;
            this.$store.state.showFooter = true;
            this.$store.state.hideConfigButton = false;
            body.classList.remove("profile-overview");
        },
    },
};
</script>
<style scoped>
.custom-alert {
    color: white;
    padding: 0.5rem;
    /* Reduce padding */

}
</style>