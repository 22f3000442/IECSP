export default {
    template : `
    <div>
        <input placeholder="username"  v-model="username"/>  
        <input placeholder="password"  v-model="password"/>  
        <button class='btn btn-primary' @click="submitLogin"> Login </button>
    </div>
    `,
    data(){
        return {
            username : null,
            password : null,
        } 
    },
    methods : {
        async submitLogin(){
            const res = await fetch(location.origin+'/login',
             {
                 method : 'POST',
                 headers: {'Content-Type' : 'application/json'}, 
                 body : JSON.stringify({'username': this.username,'password': this.password})
                })
            if (res.ok){
                console.log('we are logged in')
                const data = await res.json()
                console.log(data)
            }
        }
    }
}