<template>
	<section class="story-wrap">
		<article
			v-if="currentItem === -1"
			class="story-page story-current story-disabled"
		>
			<section class="story-main story-cover">
				<img
					class="story-cover__img"
					v-if="this.coverImage"
					:src="`${imgSrc}${filterMedia(this.coverImage)}`"
					:alt="`${this.bookName}`"
				/>
			</section>
			<section class="story-start">
				<button @click="startPage" class="btn story-start-btn">
					시작하기
				</button>
			</section>
		</article>
		<article
			:data-index="index"
			:key="index"
			v-for="(story, index) in stories"
			class="story-page hidden"
			:class="[currentItem === index ? 'story-abled' : 'story-disabled']"
		>
			<section v-if="!story.question" class="story-left">
				<div class="story-left-box">
					<img
						class="story-left__bg"
						:src="`${imgSrc}${filterMedia(story.back_image)}`"
						alt=""
					/>
					<!-- eslint-disable vue/no-use-v-if-with-v-for,vue/no-confusing-v-for-v-if -->
					<img
						:key="image.id"
						v-for="image in story.images"
						v-if="image.order === scriptNumber + 1 && !image.is_main_character"
						:src="`${imgSrc}${filterMedia(image.path)}`"
						:class="[
							`story-left__character`,
							`order${image.order}`,
							`sub${story.id}-${image.id}`,
						]"
						alt=""
					/>
					<img
						:key="image.id"
						v-for="image in story.images"
						v-if="
							image.order === scriptNumber + 1 &&
								image.is_main_character &&
								!defaultImage
						"
						:src="
							`${imgSrc}images/user/${userId}/conversion/${job}.png?count=${new Date()}`
						"
						:class="[
							`story-left__character`,
							`order${image.order}`,
							`sub${story.id}-${image.id}`,
						]"
						alt=""
					/>
					<img
						:key="image.id"
						v-for="image in story.images"
						v-if="
							image.order === scriptNumber + 1 &&
								image.is_main_character &&
								defaultImage
						"
						:src="`${imgSrc}images/character/nukkied_default2.png`"
						:class="[
							`story-left__character`,
							`order${image.order}`,
							`sub${story.id}-${image.id}`,
						]"
						alt=""
					/>
					<img
						v-if="job && defaultImage"
						:class="[`story-left__character`, `job-${job}`]"
						:src="`${imgSrc}images/character/${job}.png`"
						alt=""
					/>
					<img
						v-if="job && !defaultImage"
						:class="[`story-left__character`, `job-${job}`]"
						:src="
							`${imgSrc}images/user/${userId}/conversion/${job}.png?count=${new Date()}`
						"
						alt=""
					/>
				</div>
			</section>
			<section v-else class="story-left">
				<div class="story-left-box">
					<img
						class="story-left__bg"
						src="@/assets/images/bg/left.jpg"
						alt=""
					/>
					<img
						class="story-left__select"
						:src="`${imgSrc}images/select/${story.id}/left.png`"
						alt=""
					/>
					<button
						class="btn story-select__btn"
						@click="createSubStory(story.selects[0].substory)"
					>
						{{ story.selects[0].select }}
					</button>
				</div>
			</section>
			<StoryItem
				v-if="!story.question"
				@page-increase="currentIncrease"
				:scripts="story.scripts"
				:subId="story.id"
				:userId="userId"
				:defaultImage="defaultImage"
			/>
			<section v-else class="story-right">
				<div class="story-right-box">
					<img
						class="story-right__bg"
						src="@/assets/images/bg/right.jpg"
						alt=""
					/>
					<img
						class="story-right__select"
						:src="`${imgSrc}images/select/${story.id}/right.png`"
						alt=""
					/>
					<button
						class="btn story-select__btn"
						@click="createSubStory(story.selects[1].substory)"
					>
						{{ story.selects[1].select }}
					</button>
				</div>
			</section>
		</article>
		<section class="story-delete__btn">
			<button @click="$router.push('/bookshelf')" class="story-delete-btn">
				<i class="icon ion-md-close"></i>
			</button>
		</section>
	</section>
</template>

<script>
import bus from '@/utils/bus';
import StoryItem from '@/components/story/StoryItem.vue';
import {
	fetchSubStory,
	fetchBranch,
	fetchStory,
	deleteMyStories,
	fetchMyStory,
} from '@/api/story';
export default {
	components: {
		StoryItem,
	},
	props: {
		storyId: Number,
		myStoryId: Number,
	},
	computed: {
		imgSrc() {
			return process.env.VUE_APP_API_URL;
		},
		userSrc() {
			return '@/assets/images/user/baby_default.png';
		},
	},
	data() {
		return {
			userId: null,
			currentItem: 0,
			scriptNumber: 0,
			subNumber: -1,
			stories: [],
			nextStoryId: null,
			nextBranchId: null,
			hasBranch: null,
			finish: false,
			selectStories: [],
			coverImage: null,
			bookName: null,
			job: 0,
			defaultImage: null,
			myBook: null,
		};
	},
	destroyed() {
		if (this.myBook) {
			if (this.finish === false) {
				this.deleteBook();
			}
		}
		this.currentItem = 0;
		this.scriptNumber = 0;
		this.subNumber = -1;
		this.stories = [];
		this.nextStoryId = null;
		this.nextBranchId = null;
		this.hasBranch = null;
		this.finish = false;
		this.job = 0;
		this.defaultImage = null;
		this.selectStories = [];
	},
	beforeUpdate() {
		const playingSounds = document.querySelectorAll('.story-sound__playing');
		if (playingSounds) {
			playingSounds.forEach(playingSound => {
				playingSound.pause();
			});
		}
	},
	updated() {},
	methods: {
		resetScript() {
			this.scriptNumber = 0;
		},
		currentIncrease() {
			this.currentItem += 1;
		},
		scriptIncrease() {
			this.scriptNumber += 1;
		},
		async fetchCover() {
			try {
				const { data } = await fetchStory(this.storyId);
				this.coverImage = data.cover_image;
				this.bookName = data.name;
				this.subNumber = data.substory;
				this.createSubStory(this.subNumber);
			} catch (error) {
				bus.$emit('show:warning', '이미지를 불러오는데 실패했어요 :(');
			}
		},
		async createSubStory(num) {
			try {
				this.selectStories.push(num);
				const { data } = await fetchSubStory({
					mystory_id: this.myStoryId,
					substory_id: num,
				});
				this.hasBranch = data.has_branch;
				if (!this.hasBranch) {
					this.nextStoryId = data.next_id;
					this.nextBranchId = 0;
				} else {
					this.nextBranchId = data.next_id;
					this.nextStoryId = 0;
				}
				this.stories.push(data);
				if (this.currentItem !== 0) {
					this.currentItem += 1;
				}
			} catch (error) {
				if (this.myBook) {
					bus.$emit('show:warning', '정보를 불러오는데 실패했어요 :(');
				}
			}
		},
		async updateStory() {
			try {
				if (this.finish) {
					bus.$emit('show:finished', {
						mystory: this.myStoryId,
						selectStories: this.selectStories,
						job: this.job,
						defaultImage: Boolean(this.$route.query.default),
					});
				} else {
					if (this.nextStoryId) {
						this.selectStories.push(this.nextStoryId);
						const { data } = await fetchSubStory({
							mystory_id: this.myStoryId,
							substory_id: this.nextStoryId,
						});
						if (data.next_id === null) {
							this.finish = true;
							switch (data.scripts[0].substory) {
								case 47:
									this.job = 4;
									break;
								case 46:
									this.job = 5;
									break;
								case 45:
									this.job = 2;
									break;
								case 44:
									this.job = 1;
									break;
								case 43:
									this.job = 3;
									break;
								default:
									this.job = 0;
							}
						}
						this.hasBranch = data.has_branch;
						if (!this.hasBranch) {
							this.nextStoryId = data.next_id;
							this.nextBranchId = 0;
						} else {
							this.nextBranchId = data.next_id;
							this.nextStoryId = 0;
						}
						this.stories.push(data);
					} else if (this.nextBranchId) {
						const { data } = await fetchBranch(this.nextBranchId);
						this.stories.push(data);
					}
				}
			} catch (error) {
				bus.$emit('show:warning', '이미지를 불러오는데 실패했어요 :(');
			}
		},
		filterMedia(string) {
			if (string.includes('/media/')) {
				return string.replace('/media/', '');
			}
			return string;
		},
		startPage() {
			const startBtn = document.querySelector('.story-start-btn');
			startBtn.style.display = 'none';
			const storyCover = document.querySelectorAll('.story-page');
			setTimeout(function() {
				storyCover[0].classList.add('story-disabled');
			}, 500);
			this.currentItem = 0;
		},
		nextPage() {
			this.currentItem += 1;
		},
		async deleteStory() {
			try {
				await deleteMyStories(this.myStoryId);
				this.$router.push({ name: 'bookshelf' });
			} catch (error) {
				bus.$emit('show:warning', '책을 삭제하는데 실패했어요 :(');
			}
		},
		async deleteBook() {
			try {
				await deleteMyStories(this.myStoryId);
			} catch (error) {
				bus.$emit('show:warning', '책을 삭제하는데 실패했어요 :(');
			}
		},
		async isMyBook() {
			try {
				const temp = this.$route.params.myStoryId;
				const { data } = await fetchMyStory(temp);
				const myId = parseInt(this.$store.getters.getId);
				const otherId = parseInt(data.user.id);
				if (myId !== otherId) {
					this.myBook = false;
					const userName = data.user.child_name;
					this.$router.push('/');
					bus.$emit('show:toast', `${userName}책이 아닌거 같아요 :(`);
				}
				this.myBook = true;
			} catch (error) {
				this.myBook = false;
				this.$router.push('/');
				bus.$emit('show:toast', '잘못된 경로에요 :(');
			}
		},
	},
	created() {
		this.defaultImage = Boolean(this.$route.query.default);
		this.fetchCover();
		this.isMyBook();
	},
	mounted() {
		const id = this.$store.getters.getId;
		this.userId = parseInt(id);
		bus.$on('page-increase', this.currentIncrease);
		bus.$on('script-increase', this.scriptIncrease);
		bus.$on('script-reset', this.resetScript);
		bus.$on('next-page', this.updateStory);
	},
};
</script>

<style lang="scss">
@include common-btn();
.story-wrap {
	width: 100%;
	height: 100vh;
	position: relative;
	perspective: 1000px;
	.story-start {
		position: absolute;
		bottom: 2rem;
		left: 50%;
		width: 10rem;
		height: 4rem;
		transform: translateX(-50%);
		.story-start-btn {
			width: 10rem;
			height: 3.5rem;
			color: rgb(82, 9, 9);
			font-weight: bold;
			font-size: 1.5rem;
			border: 1px solid rgba(82, 9, 9, 0.3);
			box-shadow: 0 6px rgba(82, 9, 9, 0.8);
			background: rgb(255, 248, 220);
			cursor: pointer;
			&:active {
				background-color: rgb(202, 195, 168);
				box-shadow: 0 5px rgba(82, 9, 9, 1);
				border: none;
				transform: translateY(4px);
			}
		}
	}
}
.story-delete__btn {
	position: absolute;
	top: 3rem;
	right: 3rem;
	width: 3rem;
	height: 3rem;
	/* transform: translateX(-50%); */
	.story-delete-btn {
		border: none;
		border-radius: 50%;
		width: 3rem;
		height: 3rem;
		font-size: 1.5rem;
		background: white;
		color: black;
		cursor: pointer;
	}
}
.story-disabled {
	/* opacity: 0;
    position: absolute;
    top: -100vh;
    left: -100vw; */
	animation: fade-out 1s;
	animation-fill-mode: forwards;
}

.story-page {
	width: 100%;
	height: 100vh;
	display: flex;
	flex-wrap: wrap;
	transition: 1s;
	.story-left {
		width: 50%;
		height: 100%;
		box-shadow: 0 2px 6px 0 rgba(68, 67, 68, 0.4);
		display: flex;
		justify-content: center;
		align-items: center;
		.story-left-box {
			position: relative;
		}
		.story-left__bg {
			z-index: 1;
			width: 100%;
		}
		.story-left__character {
			z-index: 2;
			position: absolute;
			transform: translate(-50%, 50%);
		}
	}
	.story-right {
		width: 50%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		box-shadow: 0 2px 6px 0 rgba(68, 67, 68, 0.4);
		.story-right-box {
			position: relative;
		}
		.story-right__bg {
			z-index: 1;
			width: 100%;
		}
	}
	.story-main {
		width: 100%;
		height: 100%;
		box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.4);
	}
	.stroy-main::before {
		background: linear-gradient(
			to right,
			rgba(0, 0, 0, 0.2) 0px,
			transparent 5%,
			transparent 95%,
			rgba(0, 0, 0, 0.2) 100%
		);
	}
	.story-cover {
		display: flex;
		justify-content: center;
		align-items: center;
		.story-cover__img {
			height: 100%;
			object-fit: cover;
		}
	}
	.story-select__btn {
		width: 300px;
		height: 50px;
		position: absolute;
		top: 70%;
		left: 50%;
		transform: translate(-50%, 50%);
		color: white;
		font-size: 1rem;
		border: none;
		font-weight: bold;
		box-shadow: 0 8px #999;
		background: #2f4661;
		cursor: pointer;
		&:active {
			position: absolute;
			top: 70%;
			left: 50%;
			transform: translate(-50%, 60%);
			background-color: #303846;
			box-shadow: 0 5px#666;
			border: none;
		}
	}
}
.story-abled {
	/* opacity: 1;
    position: static; */
	animation: fade-in 1s;
	animation-fill-mode: forwards;
	display: flex !important;
}
.story-left__select {
	position: absolute;
	width: 300px;
	height: 300px;
	top: 18%;
	left: 50%;
	transform: translate(-50%, 50%);
}
.story-right__select {
	position: absolute;
	width: 300px;
	height: 300px;
	top: 18%;
	left: 50%;
	transform: translate(-50%, 50%);
}

.hidden {
	display: none;
	opacity: 0;
}

@keyframes fade-in {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

@keyframes fade-out {
	from {
		opacity: 1;
	}
	to {
		opacity: 0;
	}
}
</style>
