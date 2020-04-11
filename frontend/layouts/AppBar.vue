<template>
  <div>
    <v-app-bar
      fixed
      app
    >
      <v-toolbar-title v-text="title"/>
      <v-spacer />

      <v-switch
        label="Тема"
        v-model="$vuetify.theme.dark"
        class="pt-7 pr-4"
      />

    </v-app-bar>
  </div>
</template>

<script>
  import ExitButton from "../components/ExitButton";
  import utilsMixin from "../utils/utils";

  export default {
    name: "AppBar",
    components: {ExitButton},
    mixins: [utilsMixin],
    data () {
      return {
        title: 'Files To Archives',
      }
    },
    methods: {
      changeMenuState() {
        this.$emit('changeMenuState')
      }
    },
    watch: {
      '$vuetify.theme.dark': function (newVal) {
        this.storeValue('theme', newVal)
      }
    },
    mounted() {
      this.$vuetify.theme.dark = this.getValue('theme', true)
    }
  }
</script>

<style scoped>

</style>
