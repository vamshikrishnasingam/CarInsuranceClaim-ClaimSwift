import React from "react";
import { View, Text, TouchableOpacity, ScrollView } from "react-native";
import { icons } from "../constants";

const CustomTabBar = ({ selectedTab, setSelectedTab }) => {
  const tabs = [
    { label: "Personal Details", icon: icons.profile },
    { label: "Documents", icon: icons.document },
    { label: "Your Vehicles", icon: icons.car },
    { label: "Insurance", icon: icons.insurance },
    { label: "Claims", icon: icons.claim },
  ];

  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={{
        flexDirection: "row",
        justifyContent: "space-around",
        paddingVertical: 10,
        marginHorizontal: 15,
        marginTop: 10,
      }}
    >
      {tabs.map((tab, index) => (
        <TouchableOpacity
          key={index}
          onPress={() => setSelectedTab(tab.label)}
          style={{
            justifyContent: "center",
            alignItems: "center",
            padding: 10,
            marginHorizontal: 5,
          }}
        >
          <Text
            style={{
              color: selectedTab === tab.label ? "#007bff" : "#888",
              fontSize: 16,
              fontWeight: "500",
            }}
          >
            {tab.label}
          </Text>
          {/* Active tab underline */}
          {selectedTab === tab.label && (
            <View
              style={{
                marginTop: 5,
                height: 2,
                width: 30,
                backgroundColor: "#007bff",
                borderRadius: 2,
              }}
            />
          )}
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
};

export default CustomTabBar;
