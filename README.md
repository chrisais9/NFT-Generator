<div align="center">
<img width="300" src="https://www.mhaf.io/assets/icons/mhaf_full_black.svg"/>
  <h2 align="center">NFT generator</h2>
  <p align="center">Gently crafted for MHAF</p>
  <p align="center">Authored by Koo Hyong Mo</p>
</div>

## Settings
아래 파일들을 다음 포맷에 맞도록 모두 준비한다.

### config.yaml
```yaml
title: Meta Human
description: Meta Human Always Fancy

base_uri: https://ipfs.io/ipfs/Qme42XjH7tBpvqyCqQFoa6UmbXehnRbwk5NDVATCSVQvf3

# Change the seed until a million dollar collection is generated.
seed: 888

start: 1

size:
  width: 2000
  height: 2000

# Z-index order of image from bottom to top
order:
  - background
  - h_effect
  - h_faceAccessories
  - type
  - eyes
  - mouth
  - ear
  - neck
  - mask
  - hair
  - h_headgear_hair
  - faceAccessories
  - h_hair
  - clothing
  - offhand
  - headgear
  - effect
```

### config.{type_name}.yaml
config.xx.yaml
```yaml
# Number of unique images you are going to create.
number: 10

traits:
  background:
    gray:
      name: Gray
      prob: 40
    sky_blue:
      name: Sky Blue
      prob: 30
    blue:
      name: Blue
      prob: 20
    purple:
      name: Purple
      prob: 10
    .
    .
    .
    
  effect:
    smoke:
      name: Smoke
      prob: 30
    none:
      name: None
      prob: 70
```

### .env
Pinata에서 API key를 추출해 사용한다
```text
PINATA_API_KEY=
PINATA_SECRET_KEY=
```

### layer

- Type 별로 공통으로 쓰이는 레이어는 common에 넣는다
- 이름은 같지만 Type 별로 달라지는 레이어는 알맞는 폴더(xx, xy)에 넣는다
- PNG만 사용한다

폴더구조:
```text
layer		
    ㄴ Background	
      ㄴ common
      ㄴ xx
      ㄴ xy
    
    ㄴ Hair	
      ㄴ common
      ㄴ xx
      ㄴ xy
    ㄴ ....	
      ㄴ common
      ㄴ xx
      ㄴ xy
```

## Usage

### generator.py

준비된 레이어와 확률을 기반으로 NFT 이미지와 메타데이터를 만들어냄

1. 타입별 Trait 생성
2. 각 Trait의 무결성 검증
3. /metadata에 메타데이터 저장
4. Trait 기반으로 이미지 생성후 /images에 저장

### uploader.py

만들어진 NFT 이미지와 메타데이터를 자동으로 IPFS에 업로드함

1. 이미지 IPFS에 업로드
2. 메타데이터 이미지 링크 업로드된 파일의 CID로 변경
3. 수정된 메타데이터 IPFS에 업로드

