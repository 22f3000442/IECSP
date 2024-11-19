export default {
    props : ['id'],
    template : `
    <div>
    <h1> {{campaign.name}}</h1>
    <p> {{campaign.description}}</p>
    <p> {{campaign.visibility}} </p>
    <p> Budget : {{campaign.budget}} </p>
    <p> Goal :{{campaign.goals}} </p>
    <p> Sponsor Id : {{campaign.sponsor_id}} </p>
    <p> Start Date : {{formattedStartDate}} </p>
    <p> End Date : {{formattedEndDate}} </p>
    </div>

    `,
    data(){
        return {
            campaign : {},
        }
    },
    computed: {
        formattedStartDate() {
            return new Date(this.campaign.start_date).toLocaleString();
        },
        formattedEndDate() {
            return new Date(this.campaign.end_date).toLocaleString();
        }
    },
    async mounted(){
       const res = await fetch(`${location.origin}/api/campaigns/${this.id}`,{
           headers : {
               'Authentication-Token' : this.$store.state.auth_token
           }
       })
       if (res.ok){
           this.campaign  = await res.json()
       }
   }
}