export default {
    template : ` 
    <div>
    <router-link to="/"> Home </router-link>
    <router-link to="/login" v-if="!$store.state.loggedIn"> Login </router-link>
    <router-link to="/register" v-if="!$store.state.loggedIn"> Register </router-link>
    <router-link v-if="$store.state.loggedIn && $store.state.role == 'admin'" to='/admin-dashboard'>Admin Dash</router-link>
    <router-link v-if="$store.state.loggedIn && $store.state.role == 'sponsor'" to='/campaigns'>Campaigns</router-link>
    <button class="btn btn-secondary" v-if="$store.state.loggedIn" @click="$store.commit('logout')">Logout</button>

</div>
    `
}