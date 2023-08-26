---
title: "Loudness Normalization (Volume Compression)"
date: 2023-06-06
modified: 2023-08-25
original_hash: cdbaf9dbe6a2a6791fa8e6b3b5949115089934fd5dd99f73f50dedae3a8f00ba
draft: false
---

# What is the Goal?

Primarily its to bring the levels closer together while still sounding transparent.

# How Do You Obtain Transparent Compression?

Primarily its done through multiple stages instead of just one The goal is to get slight levels of gain reduction at each stage. 

Some of the compressors are aimed at a lower DB level but have a super low ratio. Such as a LA2A style compressor. Or in some cases they are meant to catch transient spikes with a fast attack and a fast release (1176).

# Final Steps In Adobe Premiere Pro (Adobe Products)

Currently my target is [-16 lufs Volume Target, Premiere Pro](/posts/16-lufs-volume-target-premiere-pro). The reason for this was because I'm aiming for the highest volume while still getting a healthy dynamic range. I've noticed hitting this rough target gets a not overly compressed feeling. Which sits better with the Audience when the focus is dialog.

in the past I've also used

1. [-14 lufs Volume Target, Highly Compressed, Premiere Pro](/posts/14-lufs-volume-target-highly-compressed-premiere-pro)
