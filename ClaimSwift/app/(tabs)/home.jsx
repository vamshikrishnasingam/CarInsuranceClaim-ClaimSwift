import { StyleSheet, Text, View, Image, FlatList } from "react-native";
import React, { useEffect, useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { images } from "../../constants";
import SearchInput from "../../components/SearchInput";
import { useGlobalContext } from "../../context/GlobalProvider";
import Trending from "../../components/Trending";
import EmptyState from "../../components/EmptyState";
import { RefreshControl } from "react-native";
import { getAllPosts, getLastestPosts } from "../../lib/appwrite";
import useAppWrite from "../../lib/useAppWrite";
import VideoCard from "../../components/VideoCard";
const Home = () => {
  const { user, setUser, setIsloggedIn } = useGlobalContext();
  const { data: posts, refetch } = useAppWrite(getAllPosts);
  const { data: latestPosts } = useAppWrite(getLastestPosts);
  const [refreshing, setRefreshing] = useState(false);
  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  return (
    <SafeAreaView className="bg-primary h-full">
      <FlatList
        data={posts}
        keyExtractor={(item, index) => item.id || index.toString()}
        renderItem={({ item }) => <VideoCard video={item} />}
        ListHeaderComponent={() => (
          <View className="flex my-6 px-4 space-y-6">
            <View className="flex justify-between items-start flex-row">
              <View>
                <Text className="text-4xl font-psemibold text-white">
                  ClaimSwift
                </Text>
                <Text className="font-pmedium text-xl text-gray-100 m-1">
                  Welcome Back, {user?.username}
                </Text>
              </View>

              <View>
                <Image
                  source={images.logoSmall}
                  className="w-10 h-10"
                  resizeMode="contain"
                />
              </View>
            </View>

            <SearchInput />

            <View className="w-full flex-1 pt-3">
              <Text className="text-lg font-pregular text-gray-100">
                Latest Videos
              </Text>
              <Trending posts={latestPosts} />
            </View>
          </View>
        )}
        ListEmptyComponent={() => (
          <EmptyState
            title="No Videos found"
            subtitle="Be the first one to upload a video"
          />
        )}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      />
    </SafeAreaView>
  );
};

export default Home;
