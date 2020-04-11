<template>
  <div>
    <v-row>
      <v-col cols="12" md="4">

        <v-card class="mt-3">
          <v-card-title>
            Выбранные файлы
          </v-card-title>

          <v-card-text>
            <v-list dense>

              <v-list-item v-for="(file, index) in files" @click="openFile(file)">

                <v-list-item-icon>
                  <v-icon class="pt-1"> mdi-file </v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                  <v-list-item-title>
                    {{ file.name }}
                  </v-list-item-title>

                  <v-list-item-subtitle v-if="file.size > 1024">
                    {{ (file.size / 1024).toFixed(1) }} kb
                  </v-list-item-subtitle>
                  <v-list-item-subtitle v-else>
                    {{ file.size }} b
                  </v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                  <v-btn icon dark @click.stop="deleteFile(index)">
                    <v-icon color="red">
                      mdi-delete
                    </v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>


            </v-list>
          </v-card-text>

          <v-card-actions>
            <v-btn icon @click="deleteAllFiles" color="black" dark title="Удалить все файлы">
              <v-icon color="black">
                mdi-delete
              </v-icon>
            </v-btn>

            <v-spacer/>

            <v-btn :loading="loadingFile" color="primary" @click="$refs.uploadFileForm.openDialogFile()">
              Добавить
            </v-btn>
            <upload-file-form @selectedFiles="addFiles" ref="uploadFileForm"/>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-spacer/>

      <v-col cols="12" md="3">
        <v-form v-model="valid">
          <v-card class="px-10">
            <v-card-text>
              <v-row>
                Осталось попыток {{ tries.all - tries.done }} из {{ tries.all }}
              </v-row>

              <v-row>
                <v-spacer/>
                <v-btn
                  title="Конвертировать"
                  @click="convert"
                  icon
                  height="80"
                  width="80"
                  style="margin-top: 40px"
                  :loading="loadingArchive"
                  :disabled="!valid || !(tries.done < tries.all)"
                >
                  <v-icon size="70" color="green">
                    mdi-arrow-right-bold-outline
                  </v-icon>
                </v-btn>
                <v-spacer/>
              </v-row>

              <v-row class="pb-6">
                <v-col cols="8" class="px-0 pb-0">
                  <v-text-field
                    label="Имя архива"
                    v-model="form.fileName"
                    :rules="[required]"
                    required
                  />
                </v-col>
                <v-col cols="4" class="pb-0">
                  <v-select
                    label="Формат"
                    v-model="form.typeName"
                    :items="archiveTypes"
                    :rules="[required]"
                    required
                  />
                </v-col>
              </v-row>

              <v-row style="position: relative">
                <v-checkbox
                  label="Сжатие файлов"
                  v-model="form.squeezeFlag"
                  hide-details
                  dense
                  style="position: absolute; margin-top: -25px;"
                />
              </v-row>

            </v-card-text>
          </v-card>
        </v-form>
      </v-col>

      <v-spacer/>

      <v-col cols="12" md="4">
        <v-card class="mt-3">
          <v-card-title>
            Архивы
          </v-card-title>

          <v-card-text>
            <v-list dense>

              <v-list-item v-for="(archive, index) in archives">

                <v-list-item-icon>
                  <v-icon class="pt-2 pl-2"> mdi-database </v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                  <v-list-item-title>
                    {{ archive.name }}
                  </v-list-item-title>


                  <v-list-item-subtitle v-if="archive.size > 1024">
                    {{ (archive.size / 1024).toFixed(1) }} kb
                  </v-list-item-subtitle>
                  <v-list-item-subtitle v-else>
                    {{ archive.size }} b
                  </v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                  <v-row>
                    <v-btn icon @click="copyLink(archive.id)" title="Копировать ссылку">
                      <v-icon>
                        mdi-content-copy
                      </v-icon>
                    </v-btn>

                    <v-btn icon dark @click="downloadArchive(archive.id)" title="Скачать архив">
                      <v-icon color="blue">
                        mdi-download
                      </v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item-action>
              </v-list-item>

            </v-list>
          </v-card-text>
        </v-card>

      </v-col>
    </v-row>
  </div>
</template>

<script>
  import UploadFileForm from "../components/common/UploadFileForm";
  import axios from 'axios';

  export default {
    name: "convert",
    components: {UploadFileForm},
    data() {
      return {
        loadingFile: false,
        loadingArchive: false,
        files: [],
        form: {
          fileName: '',
          typeName: '',
          squeezeFlag: false
        },
        valid: false,
        archiveTypes: [
          '.rar',
          '.zip'
        ],
        archives: [],
        required: value => !!value || 'Поле не может быть пустым',
        tries: {
          all: 0,
          done: 0
        }
      }
    },
    methods: {
      addFiles(files) {
        this.loadFiles(files)
      },
      deleteFile(index) {
        this.files.splice(index, 1)
      },
      deleteAllFiles() {
        this.files = []
      },
      loadFiles(files) {
        this.loadingFile = true
        let formData = new FormData();

        files.forEach((file, index) => {
          formData.append(index.toFixed(0), file);
        })

        axios.post('http://localhost:8000/query/',
          formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then(data => {
          data.data.forEach(file => this.files.push(file))
          this.loadingFile = false
        })
        .catch(function () {
          this.loadingFile = false
        });
      },
      openFile(file) {
        let url = 'localhost:8000/download_file?id=' + file.id
        window.open(url)
      },
      convert() {
        this.loadingArchive = true
        let formData = new FormData();

        formData.append('ids', JSON.stringify(this.files.map(x => x.id)))
        formData.append('fileName', this.form.fileName)
        formData.append('typeName', this.form.typeName)
        formData.append('squeezeFlag', this.form.squeezeFlag)

        axios.post('http://localhost:8000/convert/', formData,)
        .then(data => {
          this.archives.push(data.data)
          this.loadingArchive = false
          this.loadTriesCount()
        })
        .catch(function () {
          this.loadingArchive = false
        });
      },
      downloadArchive(archiveId) {
        let url = 'localhost:8000/download_archive?id=' + archiveId
        window.open(url)
      },
      copyLink(archiveId) {
        const copyToClipboard = str => {
          const el = document.createElement('textarea');
          el.value = str;
          document.body.appendChild(el);
          el.select();
          document.execCommand('copy');
          document.body.removeChild(el);
        }

        let url = 'http://localhost:8000/download_archive?id=' + archiveId
        copyToClipboard(url)

        this.$notify({
          group: 'notify',
          title: 'Ссылка скопирована',
          text: ''
        })
      },
      loadTriesCount() {
        axios.get('http://localhost:8000/check_try/')
        .then(data => {
          this.tries.all = data.data.try_count
          this.tries.done = data.data.done_try
        })
      }
    },
    mounted() {
      this.loadTriesCount()
    }
  }
</script>

<style scoped>

</style>