<template>
  <v-app>
    <v-content>
      <div class="full-page">
        <div class="song-pane">
          <div>
            <v-text-field label="Search" solo v-model="keyword"></v-text-field>
            <v-btn fab small dark absolute @click="generateCode" class="float-icon-1" :color="showCanvas? 'teal': ''">
              <v-icon dark>link</v-icon>
            </v-btn>
            <canvas ref="canvas" v-show="showCanvas"></canvas>
          </div>
          <v-card class="song-list">
            <v-list dense>
              <template v-for="(item, index) in searchedSongs">
                <v-divider :key="'a' + item.id" v-if="index > 0"></v-divider>
                <v-list-tile :key="'b' + item.id" @click="addSong(item)">
                  <v-list-tile-content>
                    <v-list-tile-title>{{item.description}}</v-list-tile-title>
                  </v-list-tile-content>
                </v-list-tile>
              </template>
            </v-list>
          </v-card>
          <v-card class="song-list">
            <v-list dense>
              <template v-for="(item, index) in listedSongs">
                <v-divider :key="'a' + item.id" v-if="index > 0"></v-divider>
                <v-list-tile :key="'b' + item.id" @click="setSong(item)">
                  <v-list-tile-content>
                    <v-list-tile-title>{{item.description}}</v-list-tile-title>
                  </v-list-tile-content>
                  <v-list-tile-action>
                    <v-btn icon ripple @click="removeSong(index)">
                      <v-icon>close</v-icon>
                    </v-btn>
                  </v-list-tile-action>
                </v-list-tile>
              </template>
            </v-list>
          </v-card>
        </div>
        <v-card class="image-page">
          <img :src="imageUrl" height="100%">
        </v-card>
      </div>
    </v-content>
  </v-app>
</template>
<script>
import axios from 'axios'
import QRCode from 'qrcode'
export default {
  data() {
    return {
      room: '',
      keyword: '',
      searchedSongs: [],
      listedSongs: [],
      imageUrl: '',
      showCanvas: false,
      showSearch: false,
    }
  },
  watch: {
    keyword(keyword) {
      this.searchedSongs = []
      if (keyword.length >= 2) {
        axios.get('/api/songs/', { params: { description: keyword } }).then(response => {
          this.searchedSongs = response.data
        })
      }
    },
  },
  methods: {
    addSong(item) {
      if (!this.listedSongs.find(song => song.id === item.id)) {
        this.listedSongs.push(item)
        axios.get(`/api/add_to_room/${this.room}/${item.id}/`)
      }
    },
    removeSong(index) {
      let item = this.listedSongs.splice(index, 1)[0]
      axios.get(`/api/remove_from_room/${this.room}/${item.id}/`)
    },
    setSong(item) {
      let image = item.chord_image || item.chord_url
      let match = image.match(/http:\/\/localhost:8000\/(.*)/)
      if (match) {
        this.imageUrl = match[1]
      } else {
        this.imageUrl = image
      }
      axios.get(`/api/songs/${item.id}/cache_song/`)
    },
    reloadSongs() {
      if (!this.room) return
      axios.get('/api/songs/', { params: { room: this.room } }).then(response => {
        this.listedSongs = response.data
      })
    },
    toggleSearch() {
      this.showSearch = !this.showSearch
    },
    generateCode() {
      this.showCanvas = !this.showCanvas
      QRCode.toCanvas(this.$refs.canvas, window.location.href, { width: 600 })
    },
  },
  created() {
    let match = window.location.hash.match(/^#(\d+)$/)
    if (!match) {
      axios.get(`/api/create_room/`).then(response => {
        this.room = response.data
        window.location.hash = '#' + this.room
      })
    } else {
      this.room = match[1]
    }
    setInterval(() => {
      this.reloadSongs()
    }, 5000)
  },
}
</script>
<style lang="css" scoped>
.song-pane >>> .v-text-field__details {
  display: none;
}
</style>
<style lang="scss" scoped>
.image-pane > img {
  max-width: 100%;
  object-fit: contain;
  margin: auto;
}
.float-icon-1 {
  right: 2px;
  top: 2px;
}
canvas {
  width: 100% !important;
  object-fit: contain;
}
@media screen and (min-width: 600px) {
  .application,
  .application--wrap,
  .v-content,
  .v-content__wrap {
    height: 100%;
  }
  .full-page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
  }
  .song-pane {
    flex-grow: 1;
    flex-basis: 0px;
    height: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
  }
  .song-list {
    flex-grow: 1;
    flex-basis: 0px;
    overflow-y: scroll;
  }
  .image-page {
    width: 50%;
    height: 100%;
  }
  canvas {
    position: absolute;
    z-index: 2;
    height: 100% !important;
    background-color: white;
  }
}
@media screen and (max-width: 600px) {
  .image-page {
    width: 100%;
    img {
      width: 100%;
    }
  }
}
</style>
