<template>
  <footer class="border-t border-black py-4 px-10 flex flex-wrap justify-between items-center bg-white">
    <div class="flex items-center space-x-8">
      <span class="text-2xl font-bold">chocolate</span>
      <div class="flex items-center space-x-2">
        <Phone class="w-6 h-6" />
        <span>04-12345678</span>
      </div>
      <div class="flex items-center space-x-2">
        <Mail class="w-6 h-6" />
        <span>chocolate@chocolate.com</span>
      </div>
    </div>
    <div class="flex space-x-4 items-center">
      <div class="w-10 h-10 bg-[#06C755] rounded-lg flex items-center justify-center text-white font-bold text-xs cursor-pointer">LINE</div>
      <div class="w-10 h-10 border border-black rounded-full flex items-center justify-center cursor-pointer">
        <Instagram class="w-6 h-6" />
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Phone, Mail, Instagram } from 'lucide-vue-next';
</script>