import {
  Text,
  View,
  FlatList,
  Image,
  TouchableOpacity,
  Alert,
  RefreshControl,
} from "react-native";
import React, { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { useGlobalContext } from "../../context/GlobalProvider";
import EmptyState from "../../components/EmptyState";
import { getUserPosts, signOut } from "../../lib/appwrite";
import useAppWrite from "../../lib/useAppWrite";
import VideoCard from "../../components/VideoCard";
import InfoBox from "../../components/InfoBox";
import { icons } from "../../constants";
import { router } from "expo-router";
import CustomTabBar from "../../components/CustomTabBar";

const Profile = () => {
  const { user, setUser, setIsLogged } = useGlobalContext();
  const { data: posts, refetch } = useAppWrite(() => getUserPosts(user.$id));
  const [selectedTab, setSelectedTab] = useState("Personal Details");
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  const logout = async () => {
    Alert.alert(
      "Logout",
      "Are you sure you want to logout?",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "OK",
          onPress: async () => {
            await signOut();
            setUser(null);
            setIsLogged(false);
            router.replace("/sign-in");
          },
        },
      ],
      { cancelable: true }
    );
  };
  const PersonalDetails = () => {
    return (
      <FlatList
        data={posts}
        keyExtractor={(item, index) => item.id || index.toString()}
        renderItem={({ item }) => <VideoCard video={item} />}
        ListEmptyComponent={() => (
          <EmptyState
            title="No Videos found"
            subtitle="No videos found for this search query"
          />
        )}
      />
    );
  };
  const renderContent = () => {
    switch (selectedTab) {
      case "Personal Details":
        return <PersonalDetails />;
      case "Documents":
        return <Text style={{ padding: 10 }}>Documents Content</Text>;
      case "Your Vehicles":
        return <Text style={{ padding: 10 }}>Your Vehicles Content</Text>;
      case "Insurance":
        return <Text style={{ padding: 10 }}>Insurance Content</Text>;
      case "Claims":
        return <Text style={{ padding: 10 }}>Claims Content</Text>;
      default:
        return null;
    }
  };

  return (
    <SafeAreaView className="bg-primary h-full">
      <View
        className="
            w-full justify-center items-center px-4 mt-6"
      >
        <View className="w-16 h-16 border border-secondary rounded-lg justify-center items-center">
          <Image
            source={{ uri: user?.avatar }}
            className="w-[90%] h-[90%] rounded-lg"
            resizeMode="cover"
          />
        </View>
        <InfoBox
          title={user?.username}
          subtitle="Member"
          containerStyles="mt-5"
          textStyles="text-2xl"
        />
        <View className="mt-5 flex-row gap-4">
          <InfoBox
            title={posts.length || 0}
            subtitle="Posts"
            containerStyles="px-4"
            textStyles="text-xl"
          />
          <InfoBox title="1.2k" subtitle="Followers" textStyles="text-xl" />
        </View>
        {/* Custom Tab Bar */}
        <CustomTabBar
          selectedTab={selectedTab}
          setSelectedTab={setSelectedTab}
        />
      </View>
      <FlatList
        ListHeaderComponent={() => (
          <View className="w-full">{renderContent()}</View>
        )}
        ListFooterComponent={() => (
          <View className="w-full justify-center items-center">
            <TouchableOpacity
              className="border border-secondary w-3/4 items-center justify-center flex flex-row rounded-xl min-h-[62px] gap-3"
              onPress={logout}
              activeOpacity={0.5}
            >
              <Image
                source={icons.logout}
                resizeMode="contain"
                className="w-7 h-7"
              />
              <View>
                <Text className="text-white font-pregular text-2xl">
                  Logout
                </Text>
              </View>
            </TouchableOpacity>
          </View>
        )}
        // ListEmptyComponent={() => (
        //   <EmptyState
        //     title="No Videos found"
        //     subtitle="No videos found for this search query"
        //   />
        // )}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      />
    </SafeAreaView>
  );
};

export default Profile;
