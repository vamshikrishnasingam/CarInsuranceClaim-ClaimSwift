import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import React from "react";

const BookMarks = () => {
  return (
    <SafeAreaView className="bg-primary h-full p-3">
      <View>
        <View>
          <Text className="text-4xl font-psemibold text-white">ClaimSwift</Text>
          <Text className="font-pmedium text-xl text-gray-100 m-1">
            Welcome Back
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default BookMarks;

const styles = StyleSheet.create({});
